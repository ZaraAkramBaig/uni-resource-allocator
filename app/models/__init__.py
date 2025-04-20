from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import models after db is initialized
from App.models.university import Institution
from App.models.SuperAdmin import Admin