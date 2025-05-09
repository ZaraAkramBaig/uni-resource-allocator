from models import db

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    program = db.Column(db.String(100), nullable=False)

    