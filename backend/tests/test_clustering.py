from unittest.mock import patch
import io

def test_get_clustering_report_no_documents(client, auth_token):
    """Test getting clustering report when there are no documents."""
    headers = {'Authorization': f'Bearer {auth_token}'}
    rv = client.get('/report/clustering', headers=headers)
    assert rv.status_code == 200
    assert rv.get_json() == {"clusters": []}

def test_get_clustering_report_with_document(client, auth_token):
    """Test getting clustering report after uploading a document."""
    headers = {'Authorization': f'Bearer {auth_token}'}
    
    # Upload a document first
    files_content = [
        b"apple banana apple orange banana apple",
        b"grape grape grape melon melon",
        b"computer science artificial intelligence machine learning",
        b"web development javascript react nodejs",
        b"data science python pandas numpy scikit-learn"
    ]
    for i, content in enumerate(files_content):
        data = {
            'file': (io.BytesIO(content), f'keywords_{i}.txt')
        }
        with patch('src.backend.services.knowledge_base.FAISS'):
            with patch('src.backend.services.knowledge_base.LlamaServerEmbeddings'):
                rv = client.post('/documents', headers=headers, content_type='multipart/form-data', data=data)
        assert rv.status_code == 201

    # Now, generate the report
    rv = client.get('/report/clustering', headers=headers)
    assert rv.status_code == 200
    report = rv.get_json()
    assert 'clusters' in report
    assert len(report['clusters']) > 0
