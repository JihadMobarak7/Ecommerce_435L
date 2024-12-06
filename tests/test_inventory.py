import pytest
from app import create_app
from app.extensions import db
from app.models import InventoryItem

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

def test_add_goods(test_client):
    response = test_client.post('/api/inventory/', json={
        "name": "Laptop",
        "category": "Electronics",
        "pricePerItem": 1000,
        "description": "High-end laptop",
        "countInStock": 50
    })
    assert response.status_code == 201

def test_update_goods(test_client):
    # First, add a good
    test_client.post('/api/inventory/', json={
        "name": "Laptop",
        "category": "Electronics",
        "pricePerItem": 1000,
        "description": "High-end laptop",
        "countInStock": 50
    })
    # Update the good
    response = test_client.put('/api/inventory/1', json={"pricePerItem": 900})
    assert response.status_code == 200