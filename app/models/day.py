from App.models import db

class Day(db.Model):
    __tablename__ = 'days'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

    timeslots = db.relationship('TimeSlot', backref='day', cascade="all, delete-orphan")