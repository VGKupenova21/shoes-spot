from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()
from services.catalog_service import Product
from services.order_service import Order, OrderItem
from services.auth_service import User
from services.cart_service import CartItem

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    from controllers.auth_controller import auth_bp
    from controllers.catalog_controller import catalog_bp
    from controllers.cart_controller import cart_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(catalog_bp)

    @app.route("/")
    def index():
        return render_template("index.html")

    return app

if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        db.create_all()
    app.run(debug=True)
