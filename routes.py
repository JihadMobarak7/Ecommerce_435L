from flask import Blueprint, request, jsonify
from models import Customer, Goods, Sales
from database import db

customer_api = Blueprint('customer_api', __name__)

# ============================================================================
# Service 1 - Customers
# ============================================================================

# Register a new customer
@customer_api.route('/register', methods=['POST'])
def register_customer():
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

# Get all customers
@customer_api.route('/', methods=['GET'])
def get_all_customers():
    customers = Customer.query.all()
    return jsonify([{
        'id': customer.id,
        'full_name': customer.full_name,
        'username': customer.username,
        'wallet_balance': customer.wallet_balance
    } for customer in customers]), 200

# Get customer by username
@customer_api.route('/<username>', methods=['GET'])
def get_customer(username):
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

# Update customer information
@customer_api.route('/<username>', methods=['PUT'])
def update_customer(username):
    customer = Customer.query.filter_by(username=username).first()
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    data = request.get_json()
    for key, value in data.items():
        if hasattr(customer, key):
            setattr(customer, key, value)
    db.session.commit()
    return jsonify({'message': 'Customer updated successfully'}), 200

# Delete customer
@customer_api.route('/<username>', methods=['DELETE'])
def delete_customer(username):
    customer = Customer.query.filter_by(username=username).first()
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message': 'Customer deleted successfully'}), 200

# Charge wallet
@customer_api.route('/<username>/charge', methods=['POST'])
def charge_wallet(username):
    customer = Customer.query.filter_by(username=username).first()
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    amount = request.get_json().get('amount', 0)
    customer.wallet_balance += amount
    db.session.commit()
    return jsonify({'message': f'{amount} charged to wallet', 'new_balance': customer.wallet_balance}), 200

# Deduct wallet
@customer_api.route('/<username>/deduct', methods=['POST'])
def deduct_wallet(username):
    customer = Customer.query.filter_by(username=username).first()
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    amount = request.get_json().get('amount', 0)
    if customer.wallet_balance < amount:
        return jsonify({'error': 'Insufficient balance'}), 400
    customer.wallet_balance -= amount
    db.session.commit()
    return jsonify({'message': f'{amount} deducted from wallet', 'new_balance': customer.wallet_balance}), 200

# ===========================================================================
# Service 3 - Sales
# ===========================================================================

# 1. Display available goods
@customer_api.route('/sales/goods', methods=['GET'])
def display_goods():
    goods = Goods.query.all()
    return jsonify([{
        'name': good.name,
        'price': good.price
    } for good in goods if good.quantity > 0]), 200

# 2. Get goods details
@customer_api.route('/sales/goods/<good_name>', methods=['GET'])
def get_good_details(good_name):
    good = Goods.query.filter_by(name=good_name).first()
    if not good:
        return jsonify({'error': 'Good not found'}), 404
    return jsonify({
        'name': good.name,
        'price': good.price,
        'quantity': good.quantity
    }), 200

# 3. Sale
@customer_api.route('/sales/purchase', methods=['POST'])
def make_sale():
    data = request.get_json()
    username = data.get('username')
    good_name = data.get('good_name')
    quantity = data.get('quantity', 1)

    # Fetch customer and good
    customer = Customer.query.filter_by(username=username).first()
    good = Goods.query.filter_by(name=good_name).first()

    # Validations
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    if not good:
        return jsonify({'error': 'Good not found'}), 404
    if good.quantity < quantity:
        return jsonify({'error': 'Not enough stock available'}), 400
    total_price = good.price * quantity
    if customer.wallet_balance < total_price:
        return jsonify({'error': 'Insufficient wallet balance'}), 400

    # Process Sale
    customer.wallet_balance -= total_price
    good.quantity -= quantity

    # Log Sale
    sale = Sales(
        customer_id=customer.id,
        good_id=good.id,
        quantity=quantity,
        total_price=total_price
    )
    db.session.add(sale)
    db.session.commit()

    return jsonify({'message': 'Purchase successful', 'remaining_balance': customer.wallet_balance}), 200

# 4. Historical purchases
@customer_api.route('/sales/history/<username>', methods=['GET'])
def purchase_history(username):
    customer = Customer.query.filter_by(username=username).first()
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    sales = Sales.query.filter_by(customer_id=customer.id).all()
    return jsonify([{
        'good_name': Goods.query.get(sale.good_id).name,
        'quantity': sale.quantity,
        'total_price': sale.total_price,
        'timestamp': sale.timestamp
    } for sale in sales]), 200