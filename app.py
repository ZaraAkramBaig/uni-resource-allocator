from flask import Flask
from flask_migrate import Migrate
from config import Config
from app.institutionRegistration import institution
from app.models import db
from app.departmentsRegistration import departmentInfo 
from app.userRegister import userInfo
from app.Auth import auth
from app.courseRegister import course_bp
from app.facultyRegister import faculty_bp
from app.programRegister import program_bp
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
    app.register_blueprint(course_bp, url_prefix='/api')
    app.register_blueprint(faculty_bp, url_prefix='/api')
    app.register_blueprint(program_bp, url_prefix='/api')
    
    return app