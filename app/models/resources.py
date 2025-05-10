from models import db

class Classroom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(50), unique=True, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    # time_slot = db.Column(db.String(50), nullable=True)
    # type = db.Column(db.String(20), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('room_type.id'), nullable=False)  # normalized type

class ClassroomSchedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    classroom_id = db.Column(db.Integer, db.ForeignKey('classroom.id'), nullable=False)
    schedule_day = db.Column(db.String(10), nullable=False)  # e.g. Monday
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)

class RoomType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

# In Classroom
# type_id = db.Column(db.Integer, db.ForeignKey('room_type.id'), nullable=False)

# In Classroom model
schedules = db.relationship('ClassroomSchedule', backref='classroom', lazy=True)
room_type = db.relationship('RoomType', backref='classrooms', lazy=True)
