import os
import requests
from flask import current_app
from langchain_community.vectorstores import FAISS
from langchain_core.embeddings import Embeddings
from typing import List
from langchain.chains import RetrievalQA
from .custom_llm import LlamaServerLLM, parse_llm_output
from langchain.prompts import PromptTemplate
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CrossEncoderReranker
from .custom_cross_encoder import LlamaServerCrossEncoder

FAISS_INDEX_PATH = 'faiss_index'

class LlamaServerEmbeddings(Embeddings):
    """Custom LangChain Embeddings class that calls the llama-server API."""
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        llama_server_url = current_app.config.get('LLAMA_SERVER_EMBEDDING_URL')
        try:
            response = requests.post(
                f"{llama_server_url}/v1/embeddings",
                json={"input": texts, "model": "ggml-org/embeddinggemma-300M-GGUF"}
            )
            response.raise_for_status()
            data = response.json()['data']
            data.sort(key=lambda e: e['index'])
            return [item['embedding'] for item in data]
        except requests.exceptions.RequestException as e:
            print(f"Error calling embedding API: {e}")
            return [[] for _ in texts]

    def embed_query(self, text: str) -> List[float]:
        llama_server_url = current_app.config.get('LLAMA_SERVER_EMBEDDING_URL')
        try:
            response = requests.post(
                f"{llama_server_url}/v1/embeddings",
                json={"input": text, "model": "ggml-org/embeddinggemma-300M-GGUF"}
            )
            response.raise_for_status()
            return response.json()['data'][0]['embedding']
        except requests.exceptions.RequestException as e:
            print(f"Error calling embedding API: {e}")
            return []

def _bing_search(query):
    """Performs a Bing search and summarizes the top 3 results."""
    bing_api_key = current_app.config.get('BING_API_KEY')
    if not bing_api_key or bing_api_key == 'your-bing-api-key':
        return [{"text": "Bing search is not configured.", "source": "system"}]

    search_url = "https://api.bing.microsoft.com/v7.0/search"
    headers = {"Ocp-Apim-Subscription-Key": bing_api_key}
    params = {"q": query, "count": 3, "textDecorations": True, "textFormat": "HTML"}
    
    try:
        response = requests.get(search_url, headers=headers, params=params)
        response.raise_for_status()
        search_results = response.json().get("webPages", {}).get("value", [])
        
        if not search_results:
            return []

        # Summarize results
        llama_server_url = current_app.config.get('LLAMA_SERVER_LLM_URL')
        summaries = []
        for result in search_results:
            summary_prompt = f"Please summarize the following text:\n\n{result['snippet']}"
            comp_response = requests.post(
                f"{llama_server_url}/v1/chat/completions",
                json={
                    "messages": [{"role": "user", "content": summary_prompt}],
                    "model": "ggml-org/Qwen3-1.7B-GGUF"
                }
            )
            comp_response.raise_for_status()
            summary = comp_response.json()['choices'][0]['message']['content']
            summaries.append({"text": parse_llm_output(summary), "source": result['url']})
        return summaries
    except requests.exceptions.RequestException as e:
        print(f"Error during Bing search or summarization: {e}")
        return []


def perform_search(user_id, query):
    """Performs semantic search with reranking and Bing fallback."""
    user_index_path = os.path.join(FAISS_INDEX_PATH, f"user_{user_id}")
    if not os.path.exists(user_index_path):
        return _bing_search(query)

    embeddings = LlamaServerEmbeddings()
    faiss_index = FAISS.load_local(user_index_path, embeddings, allow_dangerous_deserialization=True)
    
    retriever = faiss_index.as_retriever(search_kwargs={"k": 10})

    compressor = CrossEncoderReranker(model=LlamaServerCrossEncoder(), top_n=3)
    compression_retriever = ContextualCompressionRetriever(
        base_compressor=compressor, base_retriever=retriever
    )

    llm = LlamaServerLLM()

    prompt_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

    {context}

    Question: {question}
    Answer:"""
    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=compression_retriever,
        chain_type_kwargs={"prompt": PROMPT},
        return_source_documents=True,
    )

    result = qa_chain.invoke({"query": query})
    
    if not result["source_documents"]:
        return _bing_search(query)

    return [{"text": result["result"], "source": [doc.metadata.get('source', 'Unknown') for doc in result["source_documents"]]}]

import re
from collections import Counter
from ..models import Document
from langchain_community.document_loaders import TextLoader, PyPDFLoader, UnstructuredExcelLoader

# ... (rest of the file is the same until generate_keyword_report)

def generate_keyword_report(user_id):
    """
    Generates a keyword report by calculating word frequencies across all
    of the user's documents.
    """
    documents = Document.query.filter_by(user_id=user_id).all()
    if not documents:
        return {"top_keywords": []}

    # A simple list of English stop words
    stop_words = set([
        "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", 
        "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", 
        "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", 
        "theirs", "themselves", "what", "which", "who", "whom", "this", "that", 
        "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", 
        "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", 
        "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", 
        "at", "by", "for", "with", "about", "against", "between", "into", "through", 
        "during", "before", "after", "above", "below", "to", "from", "up", "down", 
        "in", "out", "on", "off", "over", "under", "again", "further", "then", 
        "once", "here", "there", "when", "where", "why", "how", "all", "any", 
        "both", "each", "few", "more", "most", "other", "some", "such", "no", 
        "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", 
        "t", "can", "will", "just", "don", "should", "now"
    ])

    full_text = ""
    for doc in documents:
        try:
            ext = doc.document_type
            if ext == 'txt':
                loader = TextLoader(doc.file_path)
            elif ext == 'pdf':
                loader = PyPDFLoader(doc.file_path)
            elif ext in ['xlsx', 'xls']:
                loader = UnstructuredExcelLoader(doc.file_path)
            else:
                continue
            
            doc_content = loader.load()
            for page in doc_content:
                full_text += page.page_content + " "
        except Exception as e:
            print(f"Error loading document for keyword report: {doc.file_path}, {e}")

    # Clean and count words
    words = re.findall(r'\b\w+\b', full_text.lower())
    filtered_words = [word for word in words if word not in stop_words and not word.isdigit()]
    word_counts = Counter(filtered_words)
    
    top_keywords = [word for word, count in word_counts.most_common(10)]
    
    return {"top_keywords": top_keywords}