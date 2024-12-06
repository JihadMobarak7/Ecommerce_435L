from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Review
from app.schemas import ReviewSchema
from sqlalchemy import text
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity

# Define blueprint
review_bp = Blueprint('review_bp', __name__, url_prefix='/api/reviews')

# ===============================
# Service 4 - Review Endpoints
# ===============================

# 1. Submit a new review
@review_bp.route('/', methods=['POST'])
def submit_review():
    schema = ReviewSchema()
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400

    # Proceed with logic if validation passes
    new_review = Review(**data)
    db.session.add(new_review)
    db.session.commit()
    return jsonify({'message': 'Review added successfully', 'id': new_review.id}), 201

# 2. Update a review
@review_bp.route('/<int:review_id>', methods=['PUT'])
def update_review(review_id):
    data = request.get_json()
    review = Review.query.get(review_id)
    if review:
        try:
            review.rating = data.get('rating', review.rating)
            review.comment = data.get('comment', review.comment)
            db.session.commit()
            return jsonify({
                'id': review.id,
                'product_id': review.product_id,
                'user_id': review.user_id,
                'rating': review.rating,
                'comment': review.comment
            }), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    else:
        return jsonify({'error': 'Review not found'}), 404

# 3. Delete a review
@review_bp.route('/<int:review_id>', methods=['DELETE'])
@jwt_required()
def delete_review(review_id):
    current_user = get_jwt_identity()
    review = Review.query.get(review_id)
    if not review or review.user_id != current_user:
        return jsonify({'error': 'Unauthorized'}), 403

    db.session.delete(review)
    db.session.commit()
    return jsonify({'message': 'Review deleted successfully'}), 200

@review_bp.route('/product/<int:product_id>', methods=['GET'])
def get_product_reviews(product_id):
    reviews = Review.query.filter_by(product_id=product_id).all()
    if not reviews:
        return jsonify([]), 200  # No reviews, but the route exists
    return jsonify([
        {
            'id': review.id,
            'product_id': review.product_id,
            'user_id': review.user_id,
            'rating': review.rating,
            'comment': review.comment
        } for review in reviews
    ]), 200

# 5. Get all reviews by a user
@review_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_reviews(user_id):
    reviews = Review.query.filter_by(user_id=user_id).all()
    return jsonify([
        {
            'id': review.id,
            'product_id': review.product_id,
            'rating': review.rating,
            'comment': review.comment
        } for review in reviews
    ]), 200
    
@review_bp.route('/health', methods=['GET'])
def review_health_check():
    try:
        db.session.execute(text('SELECT 1'))
        return {"status": "ok", "service": "Review Service"}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500