import pytest
from src.backend.app import create_app
from src.backend.models import db

@pytest.fixture(scope='function')
def app():
    """Create and configure a new app instance for each test."""
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "JWT_SECRET_KEY": "test-secret-key"
    })

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture(scope='function')
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture(scope='function')
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()

@pytest.fixture(scope='function')
def auth_token(client):
    """Fixture to register and login a user, returns auth token."""
    res = client.post('/auth/register', json={'username': 'testuser', 'password': 'password'})
    assert res.status_code == 201

    res = client.post('/auth/login', json={'username': 'testuser', 'password': 'password'})
    assert res.status_code == 200
    return res.get_json()['access_token']
