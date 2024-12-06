"""
This module defines the Review Service, which manages operations related to product reviews, 
including creating, updating, deleting, and fetching reviews.

Endpoints:
    - /: Submit a new review.
    - /<review_id>: Update or delete a review.
    - /product/<product_id>: Get all reviews for a specific product.
    - /user/<user_id>: Get all reviews submitted by a specific user.
    - /health: Perform a health check for the Review Service.
"""

from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Review
from app.schemas import ReviewSchema
from sqlalchemy import text
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity

# Define blueprint
review_bp = Blueprint('review_bp', __name__, url_prefix='/api/reviews')

@review_bp.route('/', methods=['POST'])
def submit_review():
    """
    Submit a new review for a product.

    Request Body:
        - product_id (int): ID of the product being reviewed.
        - user_id (int): ID of the user submitting the review.
        - rating (int): Rating given to the product (1-5).
        - comment (str, optional): Review comment.

    Returns:
        - 201: Success message with the review ID.
        - 400: Validation error message if input data is invalid.
    """
    schema = ReviewSchema()
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400

    new_review = Review(**data)
    db.session.add(new_review)
    db.session.commit()
    return jsonify({'message': 'Review added successfully', 'id': new_review.id}), 201

@review_bp.route('/<int:review_id>', methods=['PUT'])
def update_review(review_id):
    """
    Update an existing review.

    Path Parameters:
        - review_id (int): ID of the review to update.

    Request Body:
        - rating (int, optional): Updated rating (1-5).
        - comment (str, optional): Updated comment.

    Returns:
        - 200: Success message with updated review details.
        - 404: Error message if the review is not found.
        - 400: Error message if an exception occurs during the update.
    """
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

@review_bp.route('/<int:review_id>', methods=['DELETE'])
@jwt_required()
def delete_review(review_id):
    """
    Delete a review. Only the review's author can delete it.

    Path Parameters:
        - review_id (int): ID of the review to delete.

    Returns:
        - 200: Success message if the review is deleted.
        - 403: Error message if the user is unauthorized to delete the review.
    """
    current_user = get_jwt_identity()
    review = Review.query.get(review_id)
    if not review or review.user_id != current_user:
        return jsonify({'error': 'Unauthorized'}), 403

    db.session.delete(review)
    db.session.commit()
    return jsonify({'message': 'Review deleted successfully'}), 200

@review_bp.route('/product/<int:product_id>', methods=['GET'])
def get_product_reviews(product_id):
    """
    Get all reviews for a specific product.

    Path Parameters:
        - product_id (int): ID of the product.

    Returns:
        - 200: A list of reviews for the product.
        - []: An empty list if no reviews are found.
    """
    reviews = Review.query.filter_by(product_id=product_id).all()
    if not reviews:
        return jsonify([]), 200
    return jsonify([
        {
            'id': review.id,
            'product_id': review.product_id,
            'user_id': review.user_id,
            'rating': review.rating,
            'comment': review.comment
        } for review in reviews
    ]), 200

@review_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_reviews(user_id):
    """
    Get all reviews submitted by a specific user.

    Path Parameters:
        - user_id (int): ID of the user.

    Returns:
        - 200: A list of reviews submitted by the user.
    """
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
    """
    Check if the Review Service is healthy.

    Returns:
        - 200: A success message if the service is healthy.
        - 500: An error message if there is an issue.
    """
    try:
        db.session.execute(text('SELECT 1'))
        return {"status": "ok", "service": "Review Service"}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500