from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.courses import courses
from app.extensions import db
from app.models import Course


@courses.route("/")
@login_required
def list_courses():
    all_courses = Course.query.all()
    return render_template("courses/courses.html", courses=all_courses)


@courses.route("/add", methods=["GET", "POST"])
@login_required
def add_course():
    if request.method == "POST":
        course_code = request.form.get("course_code", "").strip()
        title = request.form.get("title", "").strip()
        credit_hours = request.form.get("credit_hours", "").strip()

        if not course_code or not title or not credit_hours:
            flash("All fields are required.", "danger")
            return render_template("courses/add_course.html")

        existing_course = Course.query.filter_by(course_code=course_code).first()
        if existing_course:
            flash("Course code already exists.", "warning")
            return render_template("courses/add_course.html")

        try:
            credit_hours = int(credit_hours)
        except ValueError:
            flash("Credit hours must be a number.", "danger")
            return render_template("courses/add_course.html")

        course = Course(
            course_code=course_code,
            title=title,
            credit_hours=credit_hours
        )

        db.session.add(course)
        db.session.commit()

        flash("Course added successfully.", "success")
        return redirect(url_for("courses.list_courses"))

    return render_template("courses/add_course.html")


@courses.route("/edit/<int:course_id>", methods=["GET", "POST"])
@login_required
def edit_course(course_id):
    course = Course.query.get_or_404(course_id)

    if request.method == "POST":
        course_code = request.form.get("course_code", "").strip()
        title = request.form.get("title", "").strip()
        credit_hours = request.form.get("credit_hours", "").strip()

        if not course_code or not title or not credit_hours:
            flash("All fields are required.", "danger")
            return render_template("courses/edit_course.html", course=course)

        existing_course = Course.query.filter_by(course_code=course_code).first()
        if existing_course and existing_course.id != course.id:
            flash("Course code already exists.", "warning")
            return render_template("courses/edit_course.html", course=course)

        try:
            credit_hours = int(credit_hours)
        except ValueError:
            flash("Credit hours must be a number.", "danger")
            return render_template("courses/edit_course.html", course=course)

        course.course_code = course_code
        course.title = title
        course.credit_hours = credit_hours

        db.session.commit()
        flash("Course updated successfully.", "success")
        return redirect(url_for("courses.list_courses"))

    return render_template("courses/edit_course.html", course=course)


@courses.route("/delete/<int:course_id>", methods=["POST"])
@login_required
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)

    db.session.delete(course)
    db.session.commit()

    flash("Course deleted successfully.", "info")
    return redirect(url_for("courses.list_courses"))