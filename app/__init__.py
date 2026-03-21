from flask import Flask
from config import Config
from app.extensions import db, migrate, login_manager
from app.models import User


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in first."
    login_manager.login_message_category = "warning"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.auth.routes import auth
    from app.main.routes import main
    from app.students.routes import students
    from app.api.routes import api
    from app.courses.routes import courses
    from app.users.routes import users

    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(students, url_prefix="/students")
    app.register_blueprint(api, url_prefix="/api")
    app.register_blueprint(courses, url_prefix="/courses")
    app.register_blueprint(users, url_prefix="/users")

    with app.app_context():
        db.create_all()

    return app