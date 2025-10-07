from unittest.mock import patch
import io

def test_get_keyword_report_no_documents(client, auth_token):
    """Test getting keyword report when there are no documents."""
    headers = {'Authorization': f'Bearer {auth_token}'}
    rv = client.get('/report/keywords', headers=headers)
    assert rv.status_code == 200
    assert rv.get_json() == {"top_keywords": []}

def test_get_keyword_report_with_document(client, auth_token):
    """Test getting keyword report after uploading a document."""
    headers = {'Authorization': f'Bearer {auth_token}'}
    
    # Upload a document first
    file_content = b"apple banana apple orange banana apple"
    data = {
        'file': (io.BytesIO(file_content), 'keywords.txt')
    }
    with patch('src.backend.services.knowledge_base.FAISS'):
        with patch('src.backend.services.knowledge_base.LlamaServerEmbeddings'):
            rv = client.post('/documents', headers=headers, content_type='multipart/form-data', data=data)
    assert rv.status_code == 201

    # Now, generate the report
    rv = client.get('/report/keywords', headers=headers)
    assert rv.status_code == 200
    report = rv.get_json()
    assert 'top_keywords' in report
    # The exact list might vary based on the stop words, but 'apple' and 'banana' should be there.
    assert 'apple' in report['top_keywords']
    assert 'banana' in report['top_keywords']
    assert 'orange' in report['top_keywords']
