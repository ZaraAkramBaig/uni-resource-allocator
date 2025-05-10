from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import models after db is initialized
from app.models.university import Institution
from app.models.admin import Admin