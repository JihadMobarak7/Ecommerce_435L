from flask import Flask
from flask_migrate import Migrate  # Import Flask-Migrate
from database import db
from routes import customer_api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///customers.db'  # Or your database of choice
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Register the blueprint for customer routes
app.register_blueprint(customer_api, url_prefix='/api/customers')

if __name__ == "__main__":
    app.run(debug=True)