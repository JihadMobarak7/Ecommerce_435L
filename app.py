from flask import Flask
from flask_migrate import Migrate
from database import db
from routes.customers import customer_bp
from routes.inventory import inventory_bp
from routes.sales import sales_bp
from routes.review import review_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

# Register blueprints
app.register_blueprint(customer_bp, url_prefix='/api/customers')
app.register_blueprint(inventory_bp, url_prefix='/api/inventory')
app.register_blueprint(sales_bp, url_prefix='/api/sales')
app.register_blueprint(review_bp, url_prefix='/api/reviews')

if __name__ == "__main__":
    app.run(debug=True)