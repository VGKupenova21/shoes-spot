products = [
    {
        "id": 1,
        "name": "Nike Air Force 1",
        "description": "Обувките са с гладка кожа и интересен дизайн",
        "color": "Бял",
        "sizes": [40, 41, 42, 43],
        "price": 239.99,
        "stock": 10
    },
    {
        "id": 2,
        "name": "Adidas Sambae Shoes",
        "description": "Обувки са с модерен привкус и са перфектни за спортове на закрито.",
        "color": "Черно",
        "sizes": [39, 40, 41, 42, 44],
        "price": 183.99,
        "stock": 17
    },
    {
        "id": 3,
        "name": "Nike Vomero Plus",
        "description": "Маратонките осигуряват ултракомфорт и са подходящи за бягане",
        "color": "Зелено",
        "sizes": [38, 39, 40, 41, 42],
        "price": 329.99,
        "stock": 5
    }
]

def get_all_products():
    return products

def get_product_by_id(product_id):
    return next((p for p in products if p["id"] == product_id), None)

def create_product(product_data):
    new_id = max([p["id"] for p in products], default=0) + 1
    product_data["id"] = new_id
    products.append(product_data)
    return product_data

def update_product(product_id, new_data):
    product = get_product_by_id(product_id)
    if product:
        product.update(new_data)
        return True
    return False

def delete_product(product_id):
    global products
    products = [p for p in products if p["id"] != product_id]

def search_and_filter_products(query=None, color=None, min_price=None, max_price=None, size=None, in_stock=None):
    results = products

    if query:
        results = [p for p in results if query.lower() in p["name"].lower() or query.lower() in p["color"].lower()]
    if color:
        results = [p for p in results if p["color"].lower() == color.lower()]
    if min_price is not None:
        results = [p for p in results if p["price"] >= min_price]
    if max_price is not None:
        results = [p for p in results if p["price"] <= max_price]
    if size is not None:
        results = [p for p in results if size in p["sizes"]]
    if in_stock:
        results = [p for p in results if p["stock"] > 0]

    return results

def update_product_stock(product_id, quantity=1):
    product = get_product_by_id(product_id)
    if product and product["stock"] >= quantity:
        product["stock"] -= quantity
        return True
    return False
