from app import db

class CartItem(db.Model):
    __tablename__ = "cart_items"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    product_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    price = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "product_id": self.product_id,
            "product_name": self.product_name,
            "quantity": self.quantity,
            "price": self.price
        }

def add_to_cart(username, product, quantity=1):
    existing_item = CartItem.query.filter_by(username=username, product_id=product.id).first()

    if existing_item:
        existing_item.quantity += quantity
    else:
        new_item = CartItem(
            username=username,
            product_id=product.id,
            product_name=product.name,
            quantity=quantity,
            price=product.price
        )
        db.session.add(new_item)

    db.session.commit()


def get_cart(username):
    return CartItem.query.filter_by(username=username).all()


def clear_cart(username):
    CartItem.query.filter_by(username=username).delete()
    db.session.commit()
