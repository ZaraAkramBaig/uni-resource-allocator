from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

# Initialize Flask extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from app.routes.department import bp as department_bp
    from app.routes.course import bp as course_bp
    from app.routes.faculty import bp as faculty_bp
    from app.routes.classroom import bp as classroom_bp
    from app.routes.student import bp as student_bp

    app.register_blueprint(department_bp, url_prefix='/api/departments')
    app.register_blueprint(course_bp, url_prefix='/api/courses')
    app.register_blueprint(faculty_bp, url_prefix='/api/faculty')
    app.register_blueprint(classroom_bp, url_prefix='/api/classrooms')
    app.register_blueprint(student_bp, url_prefix='/api/students')

    return app