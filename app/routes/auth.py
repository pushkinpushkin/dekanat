from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from app.db import get_db
from app.repositories.users import validate_user

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = validate_user(get_db(), username, password)
        if user:
            login_user(user)
            flash("Добро пожаловать!", "success")
            return redirect(url_for("main.index"))
        flash("Неверные учетные данные", "danger")
    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    logout_user()
    flash("Вы вышли из системы", "info")
    return redirect(url_for("auth.login"))
