import json

def test_register(client):
    """Test user registration."""
    rv = client.post('/auth/register', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    assert rv.status_code == 201
    assert 'User created successfully' in rv.get_json()['msg']

    # Test duplicate username
    rv = client.post('/auth/register', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    assert rv.status_code == 400
    assert 'Username already exists' in rv.get_json()['msg']

def test_login(client):
    """Test user login."""
    # First, register a user
    client.post('/auth/register', json={
        'username': 'loginuser',
        'password': 'loginpassword'
    })
    
    # Test successful login
    rv = client.post('/auth/login', json={
        'username': 'loginuser',
        'password': 'loginpassword'
    })
    assert rv.status_code == 200
    assert 'access_token' in rv.get_json()

    # Test bad password
    rv = client.post('/auth/login', json={
        'username': 'loginuser',
        'password': 'wrongpassword'
    })
    assert rv.status_code == 401
    assert 'Bad username or password' in rv.get_json()['msg']
