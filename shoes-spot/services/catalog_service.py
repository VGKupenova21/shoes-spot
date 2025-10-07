from app import db

class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    color = db.Column(db.String(50))
    sizes = db.Column(db.String(200))
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    category = db.Column(db.String(50))
    gender = db.Column(db.String(10))


    def get_sizes_list(self):
        if not self.sizes:
            return []
        return [s.strip() for s in self.sizes.split(",")]

def get_products_by_category(category):
    return Product.query.filter_by(category=category).all()

def get_all_products():
    return Product.query.all()

def get_product_by_id(product_id):
    return Product.query.get(product_id)

def create_product(product_data):
    sizes_value = product_data.get("sizes")

    if isinstance(sizes_value, list):
        sizes_value = ",".join(map(str, sizes_value))

    product = Product(
        name=product_data["name"],
        description=product_data["description"],
        color=product_data["color"],
        sizes=sizes_value,
        price=product_data["price"],
        stock=product_data["stock"],
        category=product_data["category"],
        gender=product_data["gender"]
    )
    db.session.add(product)
    db.session.commit()
    return product

def update_product(product_id, new_data):
    product = get_product_by_id(product_id)
    if not product:
        return False

    product.name = new_data.get("name", product.name)
    product.description = new_data.get("description", product.description)
    product.color = new_data.get("color", product.color)

    if "sizes" in new_data:
        sizes_value = new_data["sizes"]
        if isinstance(sizes_value, list):
            sizes_value = ",".join(map(str, sizes_value))
        product.sizes = sizes_value

    product.price = new_data.get("price", product.price)
    product.stock = new_data.get("stock", product.stock)
    product.category = new_data.get("category", product.category)
    product.gender = new_data.get("gender", product.gender)

    db.session.commit()
    return True

def delete_product(product_id):
    product = get_product_by_id(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()

def search_and_filter_products(query=None, color=None, min_price=None, max_price=None,
                               size=None, in_stock=None, category=None, gender=None):
    q = Product.query

    if category:
        q = q.filter(Product.category == category)
    if gender:
        q = q.filter(Product.gender == gender)
    if query:
        search = f"%{query.lower()}%"
        q = q.filter(db.or_(Product.name.ilike(search), Product.color.ilike(search)))
    if color:
        q = q.filter(Product.color.ilike(color))
    if min_price is not None:
        q = q.filter(Product.price >= min_price)
    if max_price is not None:
        q = q.filter(Product.price <= max_price)
    if in_stock:
        q = q.filter(Product.stock > 0)
    if size:
        q = q.filter(Product.sizes.like(f"%{size}%"))

    return q.all()

def update_product_stock(product_id, quantity=1):
    product = get_product_by_id(product_id)
    if product and product.stock >= quantity:
        product.stock -= quantity
        db.session.commit()
        return True
    return False