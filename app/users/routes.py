from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from werkzeug.security import generate_password_hash
from app.users import users
from app.extensions import db
from app.models import User


@users.route("/")
@login_required
def list_users():
    all_users = User.query.all()
    return render_template("users/users.html", users=all_users)


@users.route("/edit/<int:user_id>", methods=["GET", "POST"])
@login_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if not username:
            flash("Username is required.", "danger")
            return render_template("users/edit_user.html", user=user)

        existing_user = User.query.filter_by(username=username).first()
        if existing_user and existing_user.id != user.id:
            flash("Username already exists.", "warning")
            return render_template("users/edit_user.html", user=user)

        user.username = username

        if password:
            user.password_hash = generate_password_hash(password)

        db.session.commit()
        flash("User updated successfully.", "success")
        return redirect(url_for("users.list_users"))

    return render_template("users/edit_user.html", user=user)


@users.route("/delete/<int:user_id>", methods=["POST"])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    flash("User deleted successfully.", "info")
    return redirect(url_for("users.list_users"))