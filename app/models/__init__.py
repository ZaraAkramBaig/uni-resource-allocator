from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
<<<<<<< HEAD
=======

# Import models after db is initialized
from app.models.university import Institution
from app.models.admin import Admin
>>>>>>> 983c53b25afe457bc31bac56453d20c8d512c5cc
