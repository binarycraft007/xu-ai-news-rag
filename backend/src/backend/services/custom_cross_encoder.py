from typing import Any, List
from langchain_community.cross_encoders.base import BaseCrossEncoder
import requests
from flask import current_app

class LlamaServerCrossEncoder(BaseCrossEncoder):
    """Custom LangChain CrossEncoder class that calls the llama-server API."""
    client: Any = None
    model: str = "gpustack/bge-reranker-v2-m3-GGUF"

    def score(self, text_pairs: List[List[str]]) -> List[float]:
        """Score pairs of texts."""
        llama_server_url = current_app.config.get('LLAMA_SERVER_RERANKING_URL')
        scores = []
        for query, document in text_pairs:
            try:
                response = requests.post(
                    f"{llama_server_url}/rerank",
                    json={
                        "query": query,
                        "documents": [document],
                        "model": self.model,
                        "top_n": 1,
                    },
                )
                response.raise_for_status()
                results = response.json().get("results")
                if results:
                    scores.append(results[0]["relevance_score"])
                else:
                    scores.append(0.0)
            except requests.exceptions.RequestException as e:
                print(f"Error calling rerank API: {e}")
                scores.append(0.0)
        return scores
