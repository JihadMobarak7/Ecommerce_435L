import pytest
from app import create_app
from app.extensions import db
from app.models import Customer, Goods, Sales

@pytest.fixture
def test_client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create tables, including 'review'
            yield client
        with app.app_context():
            db.drop_all()

def test_display_goods(test_client):
    response = test_client.get('/api/sales/goods')
    assert response.status_code == 200

def test_make_sale(test_client):
    with test_client.application.app_context():
        customer = Customer(
            full_name="John Doe",
            username="johndoe",
            password="securepassword",
            age=30,
            address="123 Main St",
            gender="Male",
            marital_status="Single",
            wallet_balance=1000
        )
        good = Goods(name="Laptop", price=500, quantity=10)
        db.session.add(customer)
        db.session.add(good)
        db.session.commit()

    response = test_client.post('/api/sales/purchase', json={
        "username": "johndoe",
        "good_name": "Laptop",
        "quantity": 1
    })
    assert response.status_code == 200
    assert response.json['message'] == "Purchase successful"

    # Make a sale
    response = test_client.post('/api/sales/purchase', json={
        "username": "johndoe",
        "good_name": "Laptop",
        "quantity": 1
    })
    assert response.status_code == 200