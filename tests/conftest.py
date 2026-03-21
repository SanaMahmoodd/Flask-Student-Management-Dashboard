import pytest
from app import create_app
from app.extensions import db
from app.models import User, Student, Course
import json


@pytest.fixture
def app():
    app = create_app()
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///test.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        WTF_CSRF_ENABLED=False,
    )

    with app.app_context():
        db.drop_all()
        db.create_all()

        # seed user
        user = User(username="testuser")
        user.set_password("123456")
        db.session.add(user)

        # seed student
        student = Student(
            student_code="S1001",
            name="Sana",
            grades=json.dumps([90, 80, 75])
        )
        db.session.add(student)

        # seed course
        course = Course(
            course_code="C101",
            title="Python Basics",
            credit_hours=3
        )
        db.session.add(course)

        db.session.commit()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


def login(client, username="testuser", password="123456"):
    return client.post(
        "/login",
        data={"username": username, "password": password},
        follow_redirects=True
    )


def register(client, username="newuser", password="123456"):
    return client.post(
        "/register",
        data={"username": username, "password": password},
        follow_redirects=True
    )