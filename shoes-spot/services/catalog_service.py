products = [
    {
        "id": 1,
        "name": "Rebook",
        "description": "Обувките са перфектни за всякакви спортове",
        "color": "Розов",
        "sizes": [38, 39, 40, 41],
        "price": 75.99,
        "stock": 10,
        "category": "sport",
        "gender": "women"
    },
    {
        "id": 2,
        "name": "Adidas",
        "description": "Обувки са с модерен привкус и са перфектни за спортове на закрито.",
        "color": "Розов",
        "sizes": [39, 40, 41, 42, 44],
        "price": 206.99,
        "stock": 17,
        "category": "sport",
        "gender": "women"
    },
    {
        "id": 3,
        "name": "Nike InfinityRN",
        "description": "Маратонките осигуряват ултракомфорт и са подходящи за бягане",
        "color": "Бял",
        "sizes": [38, 39, 40, 41, 42],
        "price": 329.99,
        "stock": 5,
        "category": "sport",
        "gender": "men"
    },

    {
        "id": 101,
        "name": "Lasocki",
        "description": "Елегантни официални обувки за специални поводи",
        "color": "Черен",
        "sizes": [40, 41, 42, 43],
        "price": 104.99,
        "stock": 6,
        "category": "formal",
        "gender": "men"
    },
    {
        "id": 102,
        "name": "Pikolinos",
        "description": "Класически стил с високо качество",
        "color": "Кафяв",
        "sizes": [42, 43, 44],
        "price": 277.99,
        "stock": 4,
        "category": "formal",
        "gender": "men"
    },
    {
        "id": 103,
        "name": "Aldo",
        "description": "Официални мокасини за всеки ден",
        "color": "Бял",
        "sizes": [38, 40, 41],
        "price": 134.99,
        "stock": 9,
        "category": "formal",
        "gender": "women"
    },

    {
        "id": 201,
        "name": "s.Oliver",
        "description": "Удобни ежедневни обувки за всеки стил",
        "color": "Кафяв",
        "sizes": [40, 41, 42, 45],
        "price": 90.00,
        "stock": 12,
        "category": "casual",
        "gender": "men"
    },
    {
        "id": 202,
        "name": "Jana",
        "description": "Ежедневни и красиви дамски обувки",
        "color": "Бял",
        "sizes": [37, 39, 40, 41],
        "price": 73.00,
        "stock": 11,
        "category": "casual",
        "gender": "women"
    },
    {
        "id": 203,
        "name": "Geox",
        "description": "Меки и удобни за целодневно носене",
        "color": "Бял",
        "sizes": [38, 40, 41],
        "price": 140.00,
        "stock": 10,
        "category": "casual",
        "gender": "women"
    }
]


def get_products_by_category(category):
    return [p for p in products if p.get("category") == category]

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

def search_and_filter_products(query=None, color=None, min_price=None, max_price=None, size=None, in_stock=None, category=None, gender=None):
    results = products

    if category:
        results = [p for p in results if p["category"] == category]
    if gender:
        results = [p for p in results if p["gender"] == gender]
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
