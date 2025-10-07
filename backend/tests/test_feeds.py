
def test_get_feeds_empty(client, auth_token):
    """Test getting feeds when none have been added."""
    rv = client.get('/feeds', headers={'Authorization': f'Bearer {auth_token}'})
    assert rv.status_code == 200
    assert rv.get_json() == []

def test_feed_add_and_delete(client, auth_token):
    """Test a full feed add, fetch, and delete cycle."""
    headers = {'Authorization': f'Bearer {auth_token}'}
    feed_url = "https://example.com/rss.xml"

    # 1. Add a new feed
    rv = client.post('/feeds', headers=headers, json={'url': feed_url})
    assert rv.status_code == 201
    assert 'id' in rv.get_json()
    assert rv.get_json()['url'] == feed_url
    feed_id = rv.get_json()['id']

    # 2. Test getting feeds after adding
    rv = client.get('/feeds', headers=headers)
    assert rv.status_code == 200
    feeds = rv.get_json()
    assert len(feeds) == 1
    assert feeds[0]['url'] == feed_url

    # 3. Test adding a duplicate feed
    rv = client.post('/feeds', headers=headers, json={'url': feed_url})
    assert rv.status_code == 400
    assert 'Feed already exists' in rv.get_json()['msg']

    # 4. Delete the feed
    rv = client.delete(f'/feeds/{feed_id}', headers=headers)
    assert rv.status_code == 200
    assert 'Feed deleted successfully' in rv.get_json()['msg']

    # 5. Verify the feed is gone
    rv = client.get('/feeds', headers=headers)
    assert rv.status_code == 200
    assert rv.get_json() == []

def test_add_feed_no_url(client, auth_token):
    """Test adding a feed with no URL provided."""
    headers = {'Authorization': f'Bearer {auth_token}'}
    rv = client.post('/feeds', headers=headers, json={})
    assert rv.status_code == 400
    assert 'URL is required' in rv.get_json()['msg']
