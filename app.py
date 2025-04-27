from flask import Flask
from flask_migrate import Migrate
from config import Config
from App.institutionRegistration import institution
from App.models import db
from App.departmentsRegistration import departmentInfo 
from App.userRegister import userInfo
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    app.register_blueprint(institution, url_prefix='/api')
    app.register_blueprint(userInfo, url_prefix='/api')
    app.register_blueprint(departmentInfo, url_prefix='/api')

    @app.route('/')
    def index():
        return "Welcome to the University Registration System API!"

    return app