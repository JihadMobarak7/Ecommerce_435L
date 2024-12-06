import pytest
from app import create_app
from app.extensions import db
from app.models import Review, Customer, Goods
from sqlalchemy.sql import text

@pytest.fixture
def test_client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # Add seed data
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
            yield client
        with app.app_context():
            db.drop_all()

def test_submit_review(test_client):
    response = test_client.post('/api/review/', json={
        "product_id": 1,
        "user_id": 1,
        "rating": 5,
        "comment": "Great product!"
    })
    assert response.status_code == 201
    assert response.json['product_id'] == 1
    assert response.json['user_id'] == 1
    assert response.json['rating'] == 5
    assert response.json['comment'] == "Great product!"

def test_get_product_reviews(test_client, seed_data):
    response = test_client.get('/api/reviews/product/1')
    assert response.status_code == 200
    reviews = response.json
    assert len(reviews) > 0
    assert reviews[0]['product_id'] == 1
    
@pytest.fixture
def seed_data(test_client):
    with test_client.application.app_context():
        # Seed product
        db.session.execute(text("INSERT INTO product (id, name) VALUES (1, 'Test Product')"))

        # Seed review
        db.session.execute(
            text("INSERT INTO review (product_id, user_id, rating, comment, created_at, updated_at) "
                 "VALUES (1, 1, 5, 'Great product!', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)")
        )
        db.session.commit()