from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from app.auth import auth
from app.extensions import db
from app.models import User


@auth.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if not username or not password:
            flash("Username and password are required.", "danger")
            return render_template("auth/register.html")

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists.", "warning")
            return render_template("auth/register.html")

        user = User(username=username)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash("Logged in successfully.", "success")
            return redirect(url_for("main.dashboard"))

        flash("Invalid username or password.", "danger")

    return render_template("auth/login.html")


@auth.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))