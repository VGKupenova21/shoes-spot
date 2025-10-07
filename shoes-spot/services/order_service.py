from app import db
from services.cart_service import get_cart, clear_cart
from services.catalog_service import update_product_stock

class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    payment = db.Column(db.String(50), nullable=False)
    total_price = db.Column(db.Float, default=0.0)

    items = db.relationship("OrderItem", backref="order", cascade="all, delete")

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "address": self.address,
            "payment": self.payment,
            "total_price": self.total_price,
            "items": [item.to_dict() for item in self.items]
        }


class OrderItem(db.Model):
    __tablename__ = "order_items"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))
    product_id = db.Column(db.Integer, nullable=False)
    product_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "product_name": self.product_name,
            "quantity": self.quantity,
            "price": self.price
        }

class BaseOrderService:
    def place_order(self, username, address, payment):
        raise NotImplementedError

    def get_orders(self):
        raise NotImplementedError


class OrderService(BaseOrderService):
    def place_order(self, username, address, payment):
        user_cart = get_cart(username)
        if not user_cart:
            return False

        total = sum(item["product"]["price"] * item["quantity"] for item in user_cart)

        order = Order(
            username=username,
            address=address,
            payment=payment,
            total_price=total
        )
        db.session.add(order)
        db.session.commit()

        for item in user_cart:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item["product"]["id"],
                product_name=item["product"]["name"],
                quantity=item["quantity"],
                price=item["product"]["price"]
            )
            db.session.add(order_item)
            update_product_stock(item["product"]["id"], item["quantity"])

        db.session.commit()
        clear_cart(username)
        return True

    def get_orders(self):
        return [order.to_dict() for order in Order.query.all()]


class ExpressOrderService(OrderService):
    def place_order(self, username, address, payment):
        print("Обработваме експресна поръчка...")
        result = super().place_order(username, address, payment)
        if result:
            print("Експресната поръчка е приета!")
        return result
