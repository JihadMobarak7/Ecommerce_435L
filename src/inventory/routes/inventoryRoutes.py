from flask import Blueprint, request, jsonify
from db import db
from inventoryitems import InventoryItem

inventory_bp = Blueprint('inventory', __name__, url_prefix='/inventory')

@inventory_bp.route('/', methods=['POST'])
def add_goods():
    data = request.get_json()
    new_item = InventoryItem(name=data['name'], category=data['category'],
                             price_per_item=data['pricePerItem'], description=data['description'],
                             count_in_stock=data['countInStock'])
    db.session.add(new_item)
    db.session.commit()
    return jsonify(new_item), 201

@inventory_bp.route('/deduct', methods=['POST'])
def deduct_goods():
    data = request.get_json()
    item = InventoryItem.query.get(data['itemId'])
    if item and item.count_in_stock >= data['quantity']:
        item.count_in_stock -= data['quantity']
        db.session.commit()
        return jsonify(item), 200
    else:
        return jsonify({'error': 'Not enough stock or item not found'}), 400

@inventory_bp.route('/<int:item_id>', methods=['PUT'])
def update_goods(item_id):
    data = request.get_json()
    item = InventoryItem.query.get(item_id)
    if item:
        item.name = data.get('name', item.name)
        item.category = data.get('category', item.category)
        item.price_per_item = data.get('pricePerItem', item.price_per_item)
        item.description = data.get('description', item.description)
        item.count_in_stock = data.get('countInStock', item.count_in_stock)
        db.session.commit()
        return jsonify(item), 200
    else:
        return jsonify({'error': 'Item not found'}), 404
