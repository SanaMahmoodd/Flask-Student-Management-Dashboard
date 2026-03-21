from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.students import students
from app.extensions import db
from app.models import Student
import json


@students.route("/")
@login_required
def list_students():
    search = request.args.get("search", "").strip()

    if search:
        all_students = Student.query.filter(
            (Student.name.ilike(f"%{search}%")) |
            (Student.student_code.ilike(f"%{search}%"))
        ).all()
    else:
        all_students = Student.query.all()

    return render_template(
        "students/students.html",
        students=all_students,
        search=search
    )


@students.route("/add", methods=["GET", "POST"])
@login_required
def add_student():
    if request.method == "POST":
        student_code = request.form.get("student_code", "").strip()
        name = request.form.get("name", "").strip()
        grades_input = request.form.get("grades", "").strip()

        if not student_code or not name or not grades_input:
            flash("All fields are required.", "danger")
            return render_template("students/add_student.html")

        existing_student = Student.query.filter_by(student_code=student_code).first()
        if existing_student:
            flash("Student code already exists.", "warning")
            return render_template("students/add_student.html")

        try:
            grades_list = [int(x.strip()) for x in grades_input.split(",")]
        except ValueError:
            flash("Grades must be numbers separated by commas.", "danger")
            return render_template("students/add_student.html")

        student = Student(
            student_code=student_code,
            name=name,
            grades=json.dumps(grades_list)
        )

        db.session.add(student)
        db.session.commit()

        flash("Student added successfully.", "success")
        return redirect(url_for("students.list_students"))

    return render_template("students/add_student.html")


@students.route("/edit/<int:student_id>", methods=["GET", "POST"])
@login_required
def edit_student(student_id):
    student = Student.query.get_or_404(student_id)

    if request.method == "POST":
        student_code = request.form.get("student_code", "").strip()
        name = request.form.get("name", "").strip()
        grades_input = request.form.get("grades", "").strip()

        if not student_code or not name or not grades_input:
            flash("All fields are required.", "danger")
            return render_template("students/edit_student.html", student=student)

        existing_student = Student.query.filter_by(student_code=student_code).first()
        if existing_student and existing_student.id != student.id:
            flash("Student code already exists.", "warning")
            return render_template("students/edit_student.html", student=student)

        try:
            grades_list = [int(x.strip()) for x in grades_input.split(",")]
        except ValueError:
            flash("Grades must be numbers separated by commas.", "danger")
            return render_template("students/edit_student.html", student=student)

        student.student_code = student_code
        student.name = name
        student.grades = json.dumps(grades_list)

        db.session.commit()
        flash("Student updated successfully.", "success")
        return redirect(url_for("students.list_students"))

    return render_template("students/edit_student.html", student=student)


@students.route("/delete/<int:student_id>", methods=["POST"])
@login_required
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)

    db.session.delete(student)
    db.session.commit()

    flash("Student deleted successfully.", "info")
    return redirect(url_for("students.list_students"))

@students.route("/<int:student_id>")
@login_required
def student_details(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template("students/student_details.html", student=student)
