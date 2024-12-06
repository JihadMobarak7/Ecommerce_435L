"""
This module defines the Customer Service, which manages customer accounts,
including registration, authentication, wallet transactions, and CRUD operations.

Endpoints:
    - /login: Authenticate a customer and return a JWT token.
    - /register: Register a new customer account.
    - /: Retrieve a list of all customers.
    - /<username>: Retrieve, update, or delete a specific customer by username.
    - /<username>/charge: Add funds to a customer's wallet.
    - /<username>/deduct: Deduct funds from a customer's wallet.
    - /health: Perform a health check for the Customer Service.
"""

from flask import Blueprint, request, jsonify
from app.models import Customer
from app.extensions import db
from sqlalchemy.sql import text
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash

customer_bp = Blueprint('customer_bp', __name__)

@customer_bp.route('/login', methods=['POST'])
def login():
    """
    Authenticate a customer and return a JWT token.

    Request Body:
        - username (str): The username of the customer.
        - password (str): The password of the customer.

    Returns:
        - 200: A JWT token if authentication is successful.
        - 401: An error message if authentication fails.
    """
    data = request.json
    customer = Customer.query.filter_by(username=data.get('username')).first()
    if not customer or not check_password_hash(customer.password, data.get('password')):
        return jsonify({'error': 'Invalid username or password'}), 401

    access_token = create_access_token(identity=customer.id)
    return jsonify({'access_token': access_token}), 200

@customer_bp.route('/register', methods=['POST'])
def register_customer():
    """
    Register a new customer account.

    Request Body:
        - full_name (str): Full name of the customer.
        - username (str): Unique username for the customer.
        - password (str): Password for the customer.
        - age (int): Age of the customer.
        - address (str): Address of the customer.
        - gender (str): Gender of the customer.
        - marital_status (str): Marital status of the customer.

    Returns:
        - 201: A success message if the registration is successful.
        - 400: An error message if the username is already taken.
    """
    data = request.get_json()
    if Customer.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already taken'}), 400

    new_customer = Customer(
        full_name=data['full_name'],
        username=data['username'],
        password=data['password'],  # In real apps, hash passwords!
        age=data['age'],
        address=data['address'],
        gender=data['gender'],
        marital_status=data['marital_status']
    )
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({'message': 'Customer registered successfully'}), 201

@customer_bp.route('/', methods=['GET'])
def get_all_customers():
    """
    Retrieve a list of all customers.

    Returns:
        - 200: A list of all customers with basic details.
    """
    customers = Customer.query.all()
    return jsonify([{
        'id': customer.id,
        'full_name': customer.full_name,
        'username': customer.username,
        'wallet_balance': customer.wallet_balance
    } for customer in customers]), 200

@customer_bp.route('/<username>', methods=['GET'])
def get_customer(username):
    """
    Retrieve details of a specific customer by username.

    Path Parameters:
        - username (str): The username of the customer.

    Returns:
        - 200: Customer details if the customer exists.
        - 404: An error message if the customer is not found.
    """
    customer = Customer.query.filter_by(username=username).first()
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    return jsonify({
        'id': customer.id,
        'full_name': customer.full_name,
        'username': customer.username,
        'age': customer.age,
        'address': customer.address,
        'gender': customer.gender,
        'marital_status': customer.marital_status,
        'wallet_balance': customer.wallet_balance
    }), 200

@customer_bp.route('/<username>', methods=['PUT'])
def update_customer(username):
    """
    Update the details of a specific customer by username.

    Path Parameters:
        - username (str): The username of the customer.

    Request Body:
        - Fields to update (e.g., full_name, address, wallet_balance, etc.).

    Returns:
        - 200: A success message if the update is successful.
        - 404: An error message if the customer is not found.
    """
    customer = Customer.query.filter_by(username=username).first()
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    data = request.get_json()
    for key, value in data.items():
        if hasattr(customer, key):
            setattr(customer, key, value)
    db.session.commit()
    return jsonify({'message': 'Customer updated successfully'}), 200

@customer_bp.route('/<username>', methods=['DELETE'])
def delete_customer(username):
    """
    Delete a specific customer by username.

    Path Parameters:
        - username (str): The username of the customer.

    Returns:
        - 200: A success message if the deletion is successful.
        - 404: An error message if the customer is not found.
    """
    customer = Customer.query.filter_by(username=username).first()
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message': 'Customer deleted successfully'}), 200

@customer_bp.route('/<username>/charge', methods=['POST'])
def charge_wallet(username):
    """
    Add funds to a customer's wallet.

    Path Parameters:
        - username (str): The username of the customer.

    Request Body:
        - amount (float): The amount to add to the wallet.

    Returns:
        - 200: A success message with the new wallet balance.
        - 404: An error message if the customer is not found.
    """
    customer = Customer.query.filter_by(username=username).first()
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    amount = request.get_json().get('amount', 0)
    customer.wallet_balance += amount
    db.session.commit()
    return jsonify({'message': f'{amount} charged to wallet', 'new_balance': customer.wallet_balance}), 200

@customer_bp.route('/<username>/deduct', methods=['POST'])
def deduct_wallet(username):
    """
    Deduct funds from a customer's wallet.

    Path Parameters:
        - username (str): The username of the customer.

    Request Body:
        - amount (float): The amount to deduct from the wallet.

    Returns:
        - 200: A success message with the new wallet balance.
        - 404: An error message if the customer is not found.
        - 400: An error message if the balance is insufficient.
    """
    customer = Customer.query.filter_by(username=username).first()
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    amount = request.get_json().get('amount', 0)
    if customer.wallet_balance < amount:
        return jsonify({'error': 'Insufficient balance'}), 400
    customer.wallet_balance -= amount
    db.session.commit()
    return jsonify({'message': f'{amount} deducted from wallet', 'new_balance': customer.wallet_balance}), 200

@customer_bp.route('/health', methods=['GET'])
def customer_health_check():
    """
    Check if the Customer Service is healthy.

    Returns:
        - 200: A success message if the service is healthy.
        - 500: An error message if there is an issue.
    """
    try:
        db.session.execute(text('SELECT 1'))  # Explicitly wrap 'SELECT 1' with text()
        return {"status": "ok", "service": "Customer Service"}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500