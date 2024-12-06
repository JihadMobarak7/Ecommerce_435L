"""
This module defines the Sales Service, which manages operations related to product sales,
including browsing goods, making purchases, and viewing purchase history.

Endpoints:
    - /goods: List all available goods.
    - /goods/<good_name>: Get details about a specific good.
    - /purchase: Make a purchase.
    - /history/<username>: View purchase history for a specific user.
    - /health: Perform a health check for the Sales Service.
"""

from flask import Blueprint, request, jsonify
from app.models import Customer, Goods, Sales
from app.extensions import db, limiter
from app.messaging import publish_message
from sqlalchemy.sql import text

# Define the blueprint
sales_bp = Blueprint('sales_bp', __name__)

@limiter.limit("10 per minute")
@sales_bp.route('/goods', methods=['GET'])
def display_goods():
    """
    Display all available goods with a rate limit of 10 requests per minute.

    Returns:
        - 200: A list of goods with their name, price, and quantity, only if the quantity is greater than 0.
    """
    goods = Goods.query.all()
    return jsonify([
        {'name': good.name, 'price': good.price, 'quantity': good.quantity}
        for good in goods if good.quantity > 0
    ]), 200

@sales_bp.route('/goods/<good_name>', methods=['GET'])
def get_good_details(good_name):
    """
    Get details about a specific good.

    Path Parameters:
        - good_name (str): Name of the good.

    Returns:
        - 200: Details of the good (id, name, price, quantity).
        - 404: Error message if the good is not found.
    """
    good = Goods.query.filter_by(name=good_name).first()
    if not good:
        return jsonify({'error': 'Good not found'}), 404
    return jsonify({
        'id': good.id,
        'name': good.name,
        'price': good.price,
        'quantity': good.quantity
    }), 200

@sales_bp.route('/purchase', methods=['POST'])
def make_sale():
    """
    Make a purchase of a good.

    Request Body:
        - username (str): Username of the customer making the purchase.
        - good_name (str): Name of the good being purchased.
        - quantity (int, optional): Quantity of the good to purchase (default: 1).

    Returns:
        - 200: Success message with remaining wallet balance.
        - 404: Error message if the customer or good is not found.
        - 400: Error message if there is insufficient stock or wallet balance.
    """
    data = request.get_json()
    username = data.get('username')
    good_name = data.get('good_name')
    quantity = data.get('quantity', 1)

    customer = Customer.query.filter_by(username=username).first()
    good = Goods.query.filter_by(name=good_name).first()

    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    if not good:
        return jsonify({'error': 'Good not found'}), 404
    if good.quantity < quantity:
        return jsonify({'error': 'Not enough stock available'}), 400
    total_price = good.price * quantity
    if customer.wallet_balance < total_price:
        return jsonify({'error': 'Insufficient wallet balance'}), 400

    customer.wallet_balance -= total_price
    good.quantity -= quantity
    sale = Sales(customer_id=customer.id, good_id=good.id, quantity=quantity, total_price=total_price)
    db.session.add(sale)
    db.session.commit()

    message = f"Sale completed: {username} purchased {quantity} x {good_name} for ${total_price:.2f}"
    publish_message(message)

    return jsonify({'message': 'Purchase successful', 'remaining_balance': customer.wallet_balance}), 200

@sales_bp.route('/history/<username>', methods=['GET'])
def purchase_history(username):
    """
    Get the purchase history for a specific customer.

    Path Parameters:
        - username (str): Username of the customer.

    Returns:
        - 200: A list of purchases including good name, quantity, total price, and timestamp.
        - 404: Error message if the customer is not found.
    """
    customer = Customer.query.filter_by(username=username).first()
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    sales = Sales.query.filter_by(customer_id=customer.id).all()
    return jsonify([
        {
            'good_name': Goods.query.get(sale.good_id).name,
            'quantity': sale.quantity,
            'total_price': sale.total_price,
            'timestamp': sale.timestamp
        }
        for sale in sales
    ]), 200

@sales_bp.route('/health', methods=['GET'])
def sales_health_check():
    """
    Perform a health check for the Sales Service.

    Returns:
        - 200: Success message if the service is healthy.
        - 500: Error message if there is an issue.
    """
    try:
        db.session.execute(text('SELECT 1'))
        return {"status": "ok", "service": "Sales Service"}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500