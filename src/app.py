from db import app
from inventoryroutes import inventory_bp
from reviewroutes import review_bp

app.register_blueprint(inventory_bp)
app.register_blueprint(review_bp)

if __name__ == '__main__':
    app.run(debug=True)
