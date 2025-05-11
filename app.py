from flask import Flask
from flask_migrate import Migrate
from config import Config
<<<<<<< HEAD
from App.institutionRegistration import institution
from App.models import db
from App.departmentsRegistration import departmentInfo 
from App.userRegister import userInfo
from App.Auth import auth
from App.teachersRegister import teacher_bp
from App.studentRegister import student_bp
=======
from app.institutionRegistration import institution
from app.models import db
from app.departmentsRegistration import departmentInfo 
from app.userRegister import userInfo
from app.Auth import auth
from app.courseRegister import course_bp
from app.facultyRegister import faculty_bp
from app.programRegister import program_bp
>>>>>>> 983c53b25afe457bc31bac56453d20c8d512c5cc
from flask_jwt_extended import JWTManager
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    jwt = JWTManager( app)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    app.register_blueprint(institution, url_prefix='/api')
    app.register_blueprint(userInfo, url_prefix='/api')
    app.register_blueprint(departmentInfo, url_prefix='/api')
    app.register_blueprint(auth, url_prefix='/api')
<<<<<<< HEAD
    app.register_blueprint(teacher_bp, url_prefix='/api')
    app.register_blueprint(student_bp, url_prefix='/api')


=======
    app.register_blueprint(course_bp, url_prefix='/api')
    app.register_blueprint(faculty_bp, url_prefix='/api')
    app.register_blueprint(program_bp, url_prefix='/api')
    
>>>>>>> 983c53b25afe457bc31bac56453d20c8d512c5cc
    return app