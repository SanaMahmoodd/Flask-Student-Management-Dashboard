from tests.conftest import login
from app.models import Course


def test_courses_page_loads_after_login(client):
    login(client)
    response = client.get("/courses/")
    assert response.status_code == 200
    assert b"Courses Management" in response.data or b"Python Basics" in response.data


def test_add_course(client, app):
    login(client)
    response = client.post(
        "/courses/add",
        data={
            "course_code": "C202",
            "title": "Databases",
            "credit_hours": "4"
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Course added successfully" in response.data or b"Databases" in response.data

    with app.app_context():
        course = Course.query.filter_by(course_code="C202").first()
        assert course is not None
        assert course.title == "Databases"


def test_edit_course(client, app):
    login(client)

    with app.app_context():
        course = Course.query.filter_by(course_code="C101").first()
        course_id = course.id

    response = client.post(
        f"/courses/edit/{course_id}",
        data={
            "course_code": "C101",
            "title": "Python Advanced",
            "credit_hours": "3"
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Course updated successfully" in response.data or b"Python Advanced" in response.data

    with app.app_context():
        course = Course.query.get(course_id)
        assert course.title == "Python Advanced"


def test_delete_course(client, app):
    login(client)

    with app.app_context():
        course = Course.query.filter_by(course_code="C101").first()
        course_id = course.id

    response = client.post(
        f"/courses/delete/{course_id}",
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Course deleted successfully" in response.data or b"No courses" in response.data

    with app.app_context():
        course = Course.query.get(course_id)
        assert course is None