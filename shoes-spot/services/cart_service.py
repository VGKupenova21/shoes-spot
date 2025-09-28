cart = {}

def add_to_cart(username, product, quantity=1):
    if username not in cart:
        cart[username] = []

    for item in cart[username]:
        if item["product"]["id"] == product["id"]:
            item["quantity"] += quantity
            return
    cart[username].append({"product": product, "quantity": quantity})

def get_cart(username):
    return cart.get(username, [])

def clear_cart(username):
    cart[username] = []