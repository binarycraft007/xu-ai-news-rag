from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from ..models import Document
from langchain_community.document_loaders import TextLoader, PyPDFLoader, UnstructuredExcelLoader

def generate_cluster_report(user_id, n_clusters=5):
    """
    Generates a data clustering report using KMeans.
    """
    documents = Document.query.filter_by(user_id=user_id).all()
    if not documents:
        return {"clusters": []}

    full_texts = []
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
                full_texts.append(page.page_content)
        except Exception as e:
            print(f"Error loading document for clustering: {doc.file_path}, {e}")

    if not full_texts:
        return {"clusters": []}

    # Adjust n_clusters if there are fewer documents than clusters
    if len(full_texts) < n_clusters:
        n_clusters = len(full_texts)

    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(full_texts)

    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(X)

    order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names_out()

    clusters = []
    for i in range(n_clusters):
        cluster_terms = [terms[ind] for ind in order_centroids[i, :10]]
        clusters.append({"cluster_id": i, "top_terms": cluster_terms})

    return {"clusters": clusters}
