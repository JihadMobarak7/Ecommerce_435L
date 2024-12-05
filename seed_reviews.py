from app import create_app
from app.extensions import db
from app.models import Review

app = create_app()

with app.app_context():
    # Add sample reviews
    review1 = Review(product_id=1, user_id=1, rating=5, comment="Excellent product!")
    review2 = Review(product_id=1, user_id=2, rating=4, comment="Pretty good")
    review3 = Review(product_id=2, user_id=1, rating=3, comment="Average experience")

    db.session.add_all([review1, review2, review3])
    db.session.commit()
    print("Reviews seeded successfully!")