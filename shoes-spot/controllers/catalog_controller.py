from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from services.catalog_service import create_product, get_product_by_id, update_product, delete_product, \
    search_and_filter_products

catalog_bp = Blueprint("catalog", __name__, url_prefix="/catalog")

@catalog_bp.route("/")
def catalog():
    query = request.args.get("query")
    color = request.args.get("color")
    min_price = request.args.get("min_price", type=float)
    max_price = request.args.get("max_price", type=float)
    size = request.args.get("size", type=int)
    in_stock = request.args.get("in_stock")
    category = request.args.get("category")
    gender = request.args.get("gender")

    products = search_and_filter_products(
        query=query,
        color=color,
        min_price=min_price,
        max_price=max_price,
        size=size,
        in_stock=True if in_stock else False,
        category=category,
        gender=gender
    )

    return render_template("catalog.html", products=products)

@catalog_bp.route("/add", methods=["POST"])
def add():
    if not session.get("user") or session["user"]["role"] != "admin":
        flash("Само администратор може да добавя продукти!", "error")
        return redirect(url_for("catalog.catalog"))

    name = request.form.get("name")
    description = request.form.get("description")
    color = request.form.get("color")
    sizes = [int(s.strip()) for s in request.form.get("sizes").split(",")]
    price = float(request.form.get("price"))
    stock = int(request.form.get("stock"))
    category = request.form.get("category")
    gender = request.form.get("gender")

    create_product({
        "name": name,
        "description": description,
        "color": color,
        "sizes": sizes,
        "price": price,
        "stock": stock,
        "category": category,
        "gender": gender
    })

    flash("Продуктът беше добавен успешно!", "success")
    return redirect(url_for("catalog.catalog"))


@catalog_bp.route("/edit/<int:product_id>", methods=["POST"])
def edit(product_id):
    if not session.get("user") or session["user"]["role"] != "admin":
        flash("Само администратор може да редактира продукти!", "error")
        return redirect(url_for("catalog.catalog"))

    new_data = {
        "name": request.form.get("name"),
        "description": request.form.get("description"),
        "color": request.form.get("color"),
        "sizes": [int(s.strip()) for s in request.form.get("sizes").split(",")],
        "price": float(request.form.get("price")),
        "stock": int(request.form.get("stock")),
        "category": request.form.get("category"),
        "gender": request.form.get("gender")
    }
    update_product(product_id, new_data)
    flash("Продуктът е редактиран!", "success")
    return redirect(url_for("catalog.catalog"))

@catalog_bp.route("/delete/<int:product_id>")
def delete(product_id):
    if not session.get("user") or session["user"]["role"] != "admin":
        flash("Само администратор може да изтрива продукти!", "error")
        return redirect(url_for("catalog.catalog"))

    delete_product(product_id)
    flash("Продуктът е изтрит!", "info")
    return redirect(url_for("catalog.catalog"))

