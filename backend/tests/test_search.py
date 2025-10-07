from unittest.mock import patch, MagicMock

@patch('src.backend.services.search.RetrievalQA.from_chain_type')
def test_search(mock_from_chain_type, client, auth_token):
    """Test the search endpoint."""
    mock_qa_chain = MagicMock()
    mock_qa_chain.invoke.return_value = {
        "result": "This is a search result.",
        "source_documents": [MagicMock(metadata={"source": "test.txt"})]
    }
    mock_from_chain_type.return_value = mock_qa_chain
    
    headers = {'Authorization': f'Bearer {auth_token}'}

    # Test successful search
    rv = client.post('/search', headers=headers, json={'query': 'test query'})
    assert rv.status_code == 200
    assert len(rv.get_json()) == 1
    assert rv.get_json()[0]['text'] == "This is a search result."
    assert rv.get_json()[0]['source'] == ["test.txt"]

    # Test missing query
    rv = client.post('/search', headers=headers, json={})
    assert rv.status_code == 400
    assert 'Query is required' in rv.get_json()['msg']
