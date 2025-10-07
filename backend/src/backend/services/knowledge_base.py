import os
from werkzeug.utils import secure_filename
from ..models import db, Document, User
from .notification import send_notification
from langchain_community.document_loaders import TextLoader, PyPDFLoader, UnstructuredExcelLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from .search import LlamaServerEmbeddings

UPLOAD_FOLDER = 'uploads'
FAISS_INDEX_PATH = 'faiss_index'

def get_user_documents(user_id, doc_type=None, start_date=None, end_date=None):
    query = Document.query.filter_by(user_id=user_id)

    if doc_type:
        query = query.filter(Document.document_type == doc_type)
    if start_date:
        query = query.filter(Document.uploaded_at >= start_date)
    if end_date:
        query = query.filter(Document.uploaded_at <= end_date)
    
    documents = query.all()
    return [
        {
            "id": doc.id,
            "file_path": doc.file_path,
            "document_type": doc.document_type,
            "source": doc.source,
            "tags": doc.tags,
            "uploaded_at": doc.uploaded_at.isoformat()
        } for doc in documents
    ]

def add_document(user_id, file):
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    filename = secure_filename(file.filename)
    if not filename:
        return None
        
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    _, ext = os.path.splitext(filename)
    ext = ext.lower().lstrip('.')

    if ext == 'txt':
        loader = TextLoader(file_path)
    elif ext == 'pdf':
        loader = PyPDFLoader(file_path)
    elif ext in ['xlsx', 'xls']:
        loader = UnstructuredExcelLoader(file_path)
    else:
        os.remove(file_path)
        return None
    
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)

    embeddings = LlamaServerEmbeddings()
    user_index_path = os.path.join(FAISS_INDEX_PATH, f"user_{user_id}")

    if os.path.exists(user_index_path):
        faiss_index = FAISS.load_local(user_index_path, embeddings, allow_dangerous_deserialization=True)
        faiss_index.add_documents(texts)
    else:
        if not os.path.exists(FAISS_INDEX_PATH):
            os.makedirs(FAISS_INDEX_PATH)
        faiss_index = FAISS.from_documents(texts, embeddings)
    
    faiss_index.save_local(user_index_path)

    doc = Document(
        user_id=user_id,
        file_path=file_path,
        document_type=ext,
        source=filename,
        tags=""
    )
    db.session.add(doc)
    db.session.commit()

    # Send notification
    user = User.query.get(user_id)
    if user and user.username: # Assuming username is the email for simplicity
        send_notification(
            recipient=user.username,
            title="New Document Added to Your Knowledge Base",
            message_body=f"A new document '{filename}' has been successfully added."
        )

    return doc

def delete_document(user_id, doc_id):
    doc = Document.query.filter_by(id=doc_id, user_id=user_id).first()
    if doc:
        if os.path.exists(doc.file_path):
            os.remove(doc.file_path)
        
        # Note: This operation does not remove the document's vectors from the
        # local FAISS index. The vectors become "orphaned" but will not be
        # returned in search results because the corresponding metadata in the
        # SQL database has been deleted. For a production system, a vector
        # database that supports deletions or a re-indexing strategy would be
        # recommended.
        
        db.session.delete(doc)
        db.session.commit()
        return True
    return False

def batch_delete_documents(user_id, doc_ids):
    docs = Document.query.filter(Document.user_id == user_id, Document.id.in_(doc_ids)).all()
    
    deleted_count = 0
    for doc in docs:
        if os.path.exists(doc.file_path):
            os.remove(doc.file_path)
        db.session.delete(doc)
        deleted_count += 1
    
    db.session.commit()
    return deleted_count

def edit_document_metadata(user_id, doc_id, tags, source):
    doc = Document.query.filter_by(id=doc_id, user_id=user_id).first()
    if doc:
        if tags is not None:
            doc.tags = tags
        if source is not None:
            doc.source = source
        db.session.commit()
        return True
    return False