"""
This module defines the Inventory Service, which manages inventory items, 
including adding, deducting, updating stock, and performing health checks.

Endpoints:
    - /: Add new goods to the inventory.
    - /deduct: Deduct stock from existing goods in the inventory.
    - /<item_id>: Update details of a specific inventory item.
    - /health: Perform a health check for the Inventory Service.
"""

from flask import Blueprint, request, jsonify
from app.models import InventoryItem
from app.extensions import db
from sqlalchemy import text

inventory_bp = Blueprint('inventory_bp', __name__)

@inventory_bp.route('/', methods=['POST'])
def add_goods():
    """
    Add new goods to the inventory.

    Request Body:
        - name (str): Name of the item.
        - category (str): Category of the item.
        - pricePerItem (float): Price per unit of the item.
        - description (str): Description of the item.
        - countInStock (int): Quantity of the item in stock.

    Returns:
        - 201: A success message with the item ID and name.
    """
    data = request.get_json()
    new_item = InventoryItem(
        name=data['name'],
        category=data['category'],
        price_per_item=data['pricePerItem'],
        description=data['description'],
        count_in_stock=data['countInStock']
    )
    db.session.add(new_item)
    db.session.commit()
    return jsonify({'id': new_item.id, 'name': new_item.name}), 201

@inventory_bp.route('/deduct', methods=['POST'])
def deduct_goods():
    """
    Deduct stock from an existing inventory item.

    Request Body:
        - itemId (int): ID of the item to deduct stock from.
        - quantity (int): Quantity to deduct.

    Returns:
        - 200: A success message with the updated stock count.
        - 404: An error message if the item is not found.
        - 400: An error message if the stock is insufficient.
    """
    data = request.get_json()
    item = InventoryItem.query.get(data['itemId'])
    if item and item.count_in_stock >= data['quantity']:
        item.count_in_stock -= data['quantity']
        db.session.commit()
        return jsonify({'id': item.id, 'count_in_stock': item.count_in_stock}), 200
    elif not item:
        return jsonify({'error': 'Item not found'}), 404
    else:
        return jsonify({'error': 'Not enough stock'}), 400

@inventory_bp.route('/<int:item_id>', methods=['PUT'])
def update_goods(item_id):
    """
    Update details of an existing inventory item.

    Path Parameters:
        - item_id (int): ID of the item to update.

    Request Body:
        - name (str, optional): Updated name of the item.
        - category (str, optional): Updated category of the item.
        - pricePerItem (float, optional): Updated price per unit.
        - description (str, optional): Updated description.
        - countInStock (int, optional): Updated stock quantity.

    Returns:
        - 200: A success message with the updated item details.
        - 404: An error message if the item is not found.
    """
    data = request.get_json()
    item = db.session.get(InventoryItem, item_id)
    if item:
        item.name = data.get('name', item.name)
        item.category = data.get('category', item.category)
        item.price_per_item = data.get('pricePerItem', item.price_per_item)
        item.description = data.get('description', item.description)
        item.count_in_stock = data.get('countInStock', item.count_in_stock)
        db.session.commit()
        return jsonify({'id': item.id, 'name': item.name}), 200
    else:
        return jsonify({'error': 'Item not found'}), 404

@inventory_bp.route('/health', methods=['GET'])
def inventory_health_check():
    """
    Check if the Inventory Service is healthy.

    Returns:
        - 200: A success message if the service is healthy.
        - 500: An error message if there is an issue.
    """
    try:
        # Use SQLAlchemy's text function for the query
        db.session.execute(text('SELECT 1'))
        return {"status": "ok", "service": "Inventory Service"}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500