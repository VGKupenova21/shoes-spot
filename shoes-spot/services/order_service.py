from services.cart_service import get_cart, clear_cart
from services.catalog_service import products

orders = []

def place_order(username, address, payment):
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
    orders.append(order)

    clear_cart(username)
    return True