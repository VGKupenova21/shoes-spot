from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from services.auth_service import register_user, authenticate_user

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if register_user(email, password):
            flash("Регистрация успешна! Можете да влезете в профила си.", "success")
            return redirect(url_for("auth.login"))
        else:
            flash("Този имейл вече е регистриран.", "error")

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = authenticate_user(email, password)
        if user:
            session["user"] = user
            return redirect(url_for("catalog.catalog"))
        else:
            flash("Грешен имейл или парола.", "error")

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.pop("user", None)
    flash("Излязохте успешно.", "success")
    return render_template("index.html")
