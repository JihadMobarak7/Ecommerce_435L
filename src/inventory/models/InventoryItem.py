from db import db

class InventoryItem(db.Model):
    __tablename__ = 'inventory_items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    category = db.Column(db.String(80), nullable=False)
    price_per_item = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    count_in_stock = db.Column(db.Integer, nullable=False)
