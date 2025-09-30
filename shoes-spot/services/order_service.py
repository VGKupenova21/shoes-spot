from services.cart_service import get_cart, clear_cart
from services.catalog_service import products

class BaseOrderService:
    def place_order(self, username, address, payment):
        raise NotImplementedError

    def get_orders(self):
        raise NotImplementedError


class OrderService(BaseOrderService):
    def __init__(self):
        self.orders = []

    def place_order(self, username, address, payment):
        user_cart = get_cart(username)
        if not user_cart:
            return False

        for item in user_cart:
            for p in products:
                if p["id"] == item["product"]["id"]:
                    if p["stock"] >= item["quantity"]:
                        p["stock"] -= item["quantity"]
                    else:
                        return False

        order = {
            "user": username,
            "items": user_cart,
            "address": address,
            "payment": payment
        }
        self.orders.append(order)
        clear_cart(username)
        return True

    def get_orders(self):
        return self.orders


class ExpressOrderService(OrderService):
    def place_order(self, username, address, payment):
        print("Обработваме експресна поръчка...")
        result = super().place_order(username, address, payment)
        if result:
            print("Експресната поръчка е приета!")
        return result
