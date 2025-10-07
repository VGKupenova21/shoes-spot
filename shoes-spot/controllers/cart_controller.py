from flask import Blueprint, session, redirect, url_for, render_template, flash, request
from services.catalog_service import get_product_by_id, update_product_stock
from services.cart_service import add_to_cart, get_cart, clear_cart, CartItem
from app import db

cart_bp = Blueprint("cart", __name__, url_prefix="/cart")


@cart_bp.route('/')
def view_cart():
    user = session.get("user")
    if not user:
        flash("Моля, влезте в профила си, за да видите количката.", "error")
        return redirect(url_for("auth.login"))

    username = user["email"]
    cart_items = get_cart(username)

    if not cart_items:
        flash("Кошницата е празна.", "info")
        return render_template("cart.html", items=[], total=0)

    total = sum(item.price * item.quantity for item in cart_items)
    return render_template("cart.html", items=cart_items, total=total)


@cart_bp.route('/add/<int:product_id>')
def add_to_cart_route(product_id):
    user = session.get("user")
    if not user:
        flash("Моля, влезте в профила си, за да добавяте продукти.", "error")
        return redirect(url_for("auth.login"))

    product = get_product_by_id(product_id)
    if not product:
        flash("Продуктът не съществува.", "error")
        return redirect(url_for("catalog.catalog"))

    add_to_cart(user["email"], product, 1)
    flash(f"{product.name} беше добавен в кошницата.", "success")
    return redirect(url_for("catalog.catalog"))


@cart_bp.route('/remove/<int:product_id>')
def remove_from_cart(product_id):
    user = session.get("user")
    if not user:
        return redirect(url_for("auth.login"))

    username = user["email"]

    item = CartItem.query.filter_by(username=username, product_id=product_id).first()
    if item:
        db.session.delete(item)
        db.session.commit()
        flash("Продуктът беше премахнат от кошницата.", "success")
    else:
        flash("Продуктът не е намерен в количката.", "error")

    return redirect(url_for("cart.view_cart"))

@cart_bp.route('/clear')
def clear_cart_route():
    user = session.get("user")
    if not user:
        return redirect(url_for("auth.login"))

    clear_cart(user["email"])
    flash("Кошницата беше изчистена.", "success")
    return redirect(url_for("cart.view_cart"))

@cart_bp.route('/checkout', methods=["GET", "POST"])
def checkout():
    user = session.get("user")
    if not user:
        return redirect(url_for("auth.login"))

    username = user["email"]
    cart_items = get_cart(username)

    if request.method == "POST":
        address = request.form.get("address")
        payment = request.form.get("payment")

        if not cart_items:
            flash("Кошницата е празна!", "error")
            return redirect(url_for("cart.view_cart"))

        for item in cart_items:
            success = update_product_stock(item.product_id, item.quantity)
            if not success:
                flash(f"Недостатъчна наличност за {item.product_name}.", "error")
                return redirect(url_for("cart.view_cart"))

        clear_cart(username)
        flash("Поръчката е успешно направена!", "success")
        return redirect(url_for("catalog.catalog"))

    total = sum(item.price * item.quantity for item in cart_items)
    return render_template("checkout.html", items=cart_items, total=total)
