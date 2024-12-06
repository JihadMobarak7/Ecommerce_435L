import pytest
from app import create_app
from app.extensions import db
from app.models import Customer

@pytest.fixture
def test_client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
        with app.app_context():
            db.drop_all()

def test_register_customer(test_client):
    response = test_client.post('/api/customers/register', json={
        "full_name": "John Doe",
        "username": "johndoe",
        "password": "securepassword",
        "age": 30,
        "address": "123 Main St",
        "gender": "Male",
        "marital_status": "Single"
    })
    assert response.status_code == 201

def test_get_all_customers(test_client):
    response = test_client.get('/api/customers/')
    assert response.status_code == 200
    
def test_protected_route(test_client):
    response = test_client.post('/api/customers/login', json={'username': 'testuser', 'password': 'password123'})
    token = response.json['access_token']

    headers = {'Authorization': f'Bearer {token}'}
    response = test_client.get('/api/reviews/product/1', headers=headers)
    assert response.status_code == 200