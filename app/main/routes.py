from flask import render_template
from flask_login import login_required, current_user
from app.main import main
from app.models import Student, Course


@main.route("/")
def home():
    return render_template("home.html")


@main.route("/dashboard")
@login_required
def dashboard():
    students_count = Student.query.count()
    courses_count = Course.query.count()
    recent_students = Student.query.order_by(Student.id.desc()).limit(5).all()

    return render_template(
        "dashboard.html",
        user=current_user,
        students_count=students_count,
        courses_count=courses_count,
        recent_students=recent_students
    )