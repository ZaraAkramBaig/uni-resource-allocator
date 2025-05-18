from flask import Flask
from flask_migrate import Migrate
from config import Config
from App.institutionRegistration import institution
from App.models import db
from App.departmentsRegistration import departmentInfo 
from App.userRegister import userInfo
from App.Auth import auth
from App.teachersRegister import teacher_bp
from App.studentRegister import student_bp
from App.schedule import schedule
from App.notificationRegister import notification
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
    app.register_blueprint(teacher_bp, url_prefix='/api')
    app.register_blueprint(student_bp, url_prefix='/api')
    app.register_blueprint(schedule, url_prefix="/api")
    app.register_blueprint(notification, url_prefix="/api")

    return app