import io
from unittest.mock import patch

def test_get_documents_empty(client, auth_token):
    """Test getting documents when none have been uploaded."""
    rv = client.get('/documents', headers={'Authorization': f'Bearer {auth_token}'})
    assert rv.status_code == 200
    assert rv.get_json() == []

def test_document_upload_and_delete(client, auth_token):
    """Test a full document upload, fetch, and delete cycle."""
    headers = {'Authorization': f'Bearer {auth_token}'}
    
    # 1. Test successful upload
    data = {
        'file': (io.BytesIO(b"this is a test file for testing uploads"), 'test_upload.txt')
    }
    with patch('src.backend.services.knowledge_base.FAISS'):
        with patch('src.backend.services.knowledge_base.LlamaServerEmbeddings'):
            rv = client.post('/documents', headers=headers, content_type='multipart/form-data', data=data)
    
    assert rv.status_code == 201
    assert 'File uploaded successfully' in rv.get_json()['msg']

    # 2. Test getting documents after upload
    rv = client.get('/documents', headers=headers)
    assert rv.status_code == 200
    docs = rv.get_json()
    assert len(docs) == 1
    assert docs[0]['source'] == 'test_upload.txt'
    doc_id = docs[0]['id']

    # 3. Test deleting the document
    rv = client.delete(f'/documents/{doc_id}', headers=headers)
    assert rv.status_code == 200
    assert 'Document deleted successfully' in rv.get_json()['msg']

    # 4. Verify the document is gone
    rv = client.get('/documents', headers=headers)
    assert rv.status_code == 200
    assert rv.get_json() == []

def test_upload_unsupported_file_type(client, auth_token):
    """Test uploading a file with an unsupported extension."""
    headers = {'Authorization': f'Bearer {auth_token}'}
    data = {
        'file': (io.BytesIO(b"some zip data"), 'archive.zip')
    }
    rv = client.post('/documents', headers=headers, content_type='multipart/form-data', data=data)
    
    assert rv.status_code == 400
    assert 'File type not supported' in rv.get_json()['msg']

def test_upload_no_file_part(client, auth_token):
    """Test request with no file part."""
    headers = {'Authorization': f'Bearer {auth_token}'}
    rv = client.post('/documents', headers=headers)
    assert rv.status_code == 400
    assert 'No file part' in rv.get_json()['msg']

def test_upload_invalid_filename(client, auth_token):
    """Test uploading a file with a name that becomes empty after sanitization."""
    headers = {'Authorization': f'Bearer {auth_token}'}
    data = {
        'file': (io.BytesIO(b"invalid filename test"), '.../...', 'text/plain')
    }
    rv = client.post('/documents', headers=headers, content_type='multipart/form-data', data=data)
    assert rv.status_code == 400
    assert 'File type not supported' in rv.get_json()['msg']
