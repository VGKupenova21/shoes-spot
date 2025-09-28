from flask import Blueprint, session, redirect, url_for, render_template, flash, request
from services.catalog_service import get_product_by_id, update_product_stock

cart_bp = Blueprint("cart", __name__, url_prefix="/cart")

@cart_bp.route('/')
def view_cart():
    try:
        cart = session['cart']
    except KeyError:
        cart = {}
    except Exception:
        cart = {}

    cart_items = []
    total = 0

    try:
        for product_id_str, quantity in cart.items():
            product_id = int(product_id_str)
            product = get_product_by_id(product_id)
            if product:
                subtotal = product["price"] * quantity
                total += subtotal
                cart_items.append({
                    "id": product["id"],
                    "name": product["name"],
                    "price": product["price"],
                    "quantity": quantity,
                    "subtotal": subtotal
                })
    except Exception:
        cart_items = []
        total = 0

    return render_template("cart.html", cart=cart_items, total=total)


@cart_bp.route('/add/<int:product_id>')
def add_to_cart(product_id):
    product = get_product_by_id(product_id)
    if not product:
        flash("Продуктът не съществува.", "error")
        return redirect(url_for('catalog.catalog'))

    try:
        cart = session['cart']
    except KeyError:
        cart = {}
    except Exception:
        cart = {}

    try:
        cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    except Exception:
        cart = {str(product_id): 1}

    session['cart'] = cart
    flash(f"{product['name']} беше добавен в кошницата.", "success")
    return redirect(url_for('catalog.catalog'))


@cart_bp.route('/remove/<int:product_id>')
def remove_from_cart(product_id):
    try:
        cart = session['cart']
    except KeyError:
        cart = {}
    except Exception:
        cart = {}

    product_id_str = str(product_id)
    if product_id_str in cart:
        cart.pop(product_id_str)
        session['cart'] = cart
        flash("Продуктът беше премахнат от кошницата.", "success")
    else:
        flash("Продуктът не е в кошницата.", "error")

    return redirect(url_for('cart.view_cart'))


@cart_bp.route('/clear')
def clear_cart():
    session['cart'] = {}
    flash("Кошницата беше изчистена.", "success")
    return redirect(url_for('cart.view_cart'))


@cart_bp.route('/checkout', methods=["GET", "POST"])
def checkout():
    if request.method == "POST":
        address = request.form.get("address")
        payment = request.form.get("payment")

        try:
            cart = session['cart']
        except KeyError:
            cart = {}

        if not cart:
            flash("Кошницата е празна!", "error")
            return redirect(url_for('cart.view_cart'))

        for product_id_str, quantity in cart.items():
            product_id = int(product_id_str)
            success = update_product_stock(product_id, quantity)
            if not success:
                product = get_product_by_id(product_id)
                flash(f"Недостатъчна наличност за {product['name']}", "error")
                return redirect(url_for('cart.view_cart'))

        session['cart'] = {}
        flash("Поръчката е успешно направена!", "success")
        return redirect(url_for('catalog.catalog'))

    return render_template("checkout.html")
