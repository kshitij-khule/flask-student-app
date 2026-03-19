import pytest
from app import create_app
import os

@pytest.fixture
def client():
    # Tell the app we're testing
    os.environ['TESTING'] = 'true'
    
    app = create_app()
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        yield client

def test_health_check(client):
    """Test the home route returns 200"""
    response = client.get('/')
    assert response.status_code == 200