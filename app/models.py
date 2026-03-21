import json
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(50), unique=True, nullable=False)
    title = db.Column(db.String(120), nullable=False)
    credit_hours = db.Column(db.Integer, nullable=False)


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    student_code = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    grades = db.Column(db.Text, nullable=False)

    def get_grades_list(self):
        return json.loads(self.grades)

    def calculate_average(self):
        grades = self.get_grades_list()
        return round(sum(grades) / len(grades), 2) if grades else 0