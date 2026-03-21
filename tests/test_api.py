from app.models import Student, Course, User


def test_get_students_api(client):
    response = client.get("/api/students")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert "student_code" in data[0]


def test_create_student_api(client, app):
    response = client.post(
        "/api/students",
        json={
            "student_code": "S3003",
            "name": "Ahmad",
            "grades": "90,95,100"
        }
    )

    assert response.status_code == 201
    data = response.get_json()
    assert data["student_code"] == "S3003"
    assert data["average_grade"] == 95.0

    with app.app_context():
        student = Student.query.filter_by(student_code="S3003").first()
        assert student is not None


def test_update_student_api(client):
    create_response = client.post(
        "/api/students",
        json={
            "student_code": "S5555",
            "name": "Mona",
            "grades": "80,90,100"
        }
    )
    student_id = create_response.get_json()["id"]

    response = client.put(
        f"/api/students/{student_id}",
        json={
            "student_code": "S5555",
            "name": "Mona Updated",
            "grades": "100,100,100"
        }
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Mona Updated"
    assert data["average_grade"] == 100.0


def test_delete_student_api(client):
    create_response = client.post(
        "/api/students",
        json={
            "student_code": "S7777",
            "name": "Delete Me",
            "grades": "70,80,90"
        }
    )
    student_id = create_response.get_json()["id"]

    response = client.delete(f"/api/students/{student_id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Student deleted successfully"


def test_get_courses_api(client):
    response = client.get("/api/courses")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert "course_code" in data[0]


def test_create_course_api(client, app):
    response = client.post(
        "/api/courses",
        json={
            "course_code": "C303",
            "title": "Algorithms",
            "credit_hours": 3
        }
    )

    assert response.status_code == 201
    data = response.get_json()
    assert data["course_code"] == "C303"

    with app.app_context():
        course = Course.query.filter_by(course_code="C303").first()
        assert course is not None


def test_get_users_api(client):
    response = client.get("/api/users")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert "username" in data[0]


def test_create_user_api(client, app):
    response = client.post(
        "/api/users",
        json={
            "username": "apiuser",
            "password": "123456"
        }
    )

    assert response.status_code == 201
    data = response.get_json()
    assert data["username"] == "apiuser"

    with app.app_context():
        user = User.query.filter_by(username="apiuser").first()
        assert user is not None