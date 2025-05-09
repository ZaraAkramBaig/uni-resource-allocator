from models import db

class Classroom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(50), unique=True, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    time_slot = db.Column(db.String(50), nullable=True)
    type = db.Column(db.String(20), nullable=False)

   