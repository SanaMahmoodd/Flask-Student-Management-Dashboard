from tests.conftest import login
from app.models import Student


def test_students_page_requires_login(client):
    response = client.get("/students/", follow_redirects=True)
    assert response.status_code == 200
    assert b"Login" in response.data or b"Please log in first" in response.data


def test_students_page_loads_after_login(client):
    login(client)
    response = client.get("/students/")
    assert response.status_code == 200
    assert b"Students Management" in response.data or b"Sana" in response.data


def test_add_student(client, app):
    login(client)
    response = client.post(
        "/students/add",
        data={
            "student_code": "S2002",
            "name": "Ali",
            "grades": "95,88,90"
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Student added successfully" in response.data or b"Ali" in response.data

    with app.app_context():
        student = Student.query.filter_by(student_code="S2002").first()
        assert student is not None
        assert student.name == "Ali"


def test_edit_student(client, app):
    login(client)

    with app.app_context():
        student = Student.query.filter_by(student_code="S1001").first()
        student_id = student.id

    response = client.post(
        f"/students/edit/{student_id}",
        data={
            "student_code": "S1001",
            "name": "Sana Updated",
            "grades": "100,100,90"
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Student updated successfully" in response.data or b"Sana Updated" in response.data

    with app.app_context():
        student = Student.query.get(student_id)
        assert student.name == "Sana Updated"


def test_delete_student(client, app):
    login(client)

    with app.app_context():
        student = Student.query.filter_by(student_code="S1001").first()
        student_id = student.id

    response = client.post(
        f"/students/delete/{student_id}",
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Student deleted successfully" in response.data or b"No students" in response.data

    with app.app_context():
        student = Student.query.get(student_id)
        assert student is None