from flask import request, jsonify
from werkzeug.security import generate_password_hash
from app.api import api
from app.extensions import db
from app.models import Student, Course, User
import json


# -----------------------------
# Helper functions
# -----------------------------
def student_to_dict(student):
    grades_list = json.loads(student.grades)
    average = round(sum(grades_list) / len(grades_list), 2) if grades_list else 0

    return {
        "id": student.id,
        "student_code": student.student_code,
        "name": student.name,
        "grades": grades_list,
        "average_grade": average
    }


def course_to_dict(course):
    return {
        "id": course.id,
        "course_code": course.course_code,
        "title": course.title,
        "credit_hours": course.credit_hours
    }


def user_to_dict(user):
    return {
        "id": user.id,
        "username": user.username
    }


# =============================
# Students API
# =============================

@api.route("/students", methods=["POST"])
def create_student_api():
    data = request.get_json()

    try:
        student_code = data.get("student_code")
        name = data.get("name")
        grades_input = data.get("grades")

        if not student_code or not name or not grades_input:
            return jsonify({"error": "student_code, name, and grades are required"}), 400

        existing_student = Student.query.filter_by(student_code=student_code).first()
        if existing_student:
            return jsonify({"error": "Student code already exists"}), 400

        grades_list = [int(x.strip()) for x in grades_input.split(",")]

        student = Student(
            student_code=student_code,
            name=name,
            grades=json.dumps(grades_list)
        )

        db.session.add(student)
        db.session.commit()

        return jsonify(student_to_dict(student)), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@api.route("/students", methods=["GET"])
def get_students_api():
    students = Student.query.all()
    result = [student_to_dict(student) for student in students]
    return jsonify(result), 200


@api.route("/students/<int:student_id>", methods=["GET"])
def get_student_api(student_id):
    student = Student.query.get_or_404(student_id)
    return jsonify(student_to_dict(student)), 200


@api.route("/students/<int:student_id>", methods=["PUT"])
def update_student_api(student_id):
    student = Student.query.get_or_404(student_id)
    data = request.get_json()

    try:
        student_code = data.get("student_code")
        name = data.get("name")
        grades_input = data.get("grades")

        if not student_code or not name or not grades_input:
            return jsonify({"error": "student_code, name, and grades are required"}), 400

        existing_student = Student.query.filter_by(student_code=student_code).first()
        if existing_student and existing_student.id != student.id:
            return jsonify({"error": "Student code already exists"}), 400

        grades_list = [int(x.strip()) for x in grades_input.split(",")]

        student.student_code = student_code
        student.name = name
        student.grades = json.dumps(grades_list)

        db.session.commit()

        return jsonify(student_to_dict(student)), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@api.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student_api(student_id):
    student = Student.query.get_or_404(student_id)

    db.session.delete(student)
    db.session.commit()

    return jsonify({"message": "Student deleted successfully"}), 200


# =============================
# Courses API
# =============================

@api.route("/courses", methods=["POST"])
def create_course_api():
    data = request.get_json()

    try:
        course_code = data.get("course_code")
        title = data.get("title")
        credit_hours = data.get("credit_hours")

        if not course_code or not title or credit_hours is None:
            return jsonify({"error": "course_code, title, and credit_hours are required"}), 400

        existing_course = Course.query.filter_by(course_code=course_code).first()
        if existing_course:
            return jsonify({"error": "Course code already exists"}), 400

        course = Course(
            course_code=course_code,
            title=title,
            credit_hours=int(credit_hours)
        )

        db.session.add(course)
        db.session.commit()

        return jsonify(course_to_dict(course)), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@api.route("/courses", methods=["GET"])
def get_courses_api():
    courses = Course.query.all()
    result = [course_to_dict(course) for course in courses]
    return jsonify(result), 200


@api.route("/courses/<int:course_id>", methods=["GET"])
def get_course_api(course_id):
    course = Course.query.get_or_404(course_id)
    return jsonify(course_to_dict(course)), 200


@api.route("/courses/<int:course_id>", methods=["PUT"])
def update_course_api(course_id):
    course = Course.query.get_or_404(course_id)
    data = request.get_json()

    try:
        course_code = data.get("course_code")
        title = data.get("title")
        credit_hours = data.get("credit_hours")

        if not course_code or not title or credit_hours is None:
            return jsonify({"error": "course_code, title, and credit_hours are required"}), 400

        existing_course = Course.query.filter_by(course_code=course_code).first()
        if existing_course and existing_course.id != course.id:
            return jsonify({"error": "Course code already exists"}), 400

        course.course_code = course_code
        course.title = title
        course.credit_hours = int(credit_hours)

        db.session.commit()

        return jsonify(course_to_dict(course)), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@api.route("/courses/<int:course_id>", methods=["DELETE"])
def delete_course_api(course_id):
    course = Course.query.get_or_404(course_id)

    db.session.delete(course)
    db.session.commit()

    return jsonify({"message": "Course deleted successfully"}), 200


# =============================
# Users API
# =============================

@api.route("/users", methods=["POST"])
def create_user_api():
    data = request.get_json()

    try:
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"error": "username and password are required"}), 400

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({"error": "Username already exists"}), 400

        user = User(username=username)
        user.password_hash = generate_password_hash(password)

        db.session.add(user)
        db.session.commit()

        return jsonify(user_to_dict(user)), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@api.route("/users", methods=["GET"])
def get_users_api():
    users = User.query.all()
    result = [user_to_dict(user) for user in users]
    return jsonify(result), 200


@api.route("/users/<int:user_id>", methods=["GET"])
def get_user_api(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user_to_dict(user)), 200


@api.route("/users/<int:user_id>", methods=["PUT"])
def update_user_api(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()

    try:
        username = data.get("username")
        password = data.get("password")

        if not username:
            return jsonify({"error": "username is required"}), 400

        existing_user = User.query.filter_by(username=username).first()
        if existing_user and existing_user.id != user.id:
            return jsonify({"error": "Username already exists"}), 400

        user.username = username

        if password:
            user.password_hash = generate_password_hash(password)

        db.session.commit()

        return jsonify(user_to_dict(user)), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@api.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user_api(user_id):
    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User deleted successfully"}), 200