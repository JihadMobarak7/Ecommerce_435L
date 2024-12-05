from app import create_app
from app.extensions import db
from app.models import InventoryItem

app = create_app()

with app.app_context():
    # Drop and recreate the table for a clean slate (optional)
    db.drop_all()
    db.create_all()

    # Sample data for the InventoryItem table
    inventory_items = [
        InventoryItem(name="Laptop", category="Electronics", price_per_item=1000, description="High-end laptop", count_in_stock=10),
        InventoryItem(name="Phone", category="Electronics", price_per_item=500, description="Smartphone", count_in_stock=20),
        InventoryItem(name="Headphones", category="Accessories", price_per_item=100, description="Wireless headphones", count_in_stock=30),
        InventoryItem(name="Monitor", category="Electronics", price_per_item=300, description="4K monitor", count_in_stock=15),
        InventoryItem(name="Keyboard", category="Accessories", price_per_item=50, description="Mechanical keyboard", count_in_stock=25),
    ]

    # Add data to the database
    db.session.bulk_save_objects(inventory_items)
    db.session.commit()

    print("Inventory seeded successfully!")