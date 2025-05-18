from App.models import db

class TimeSlot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(20), nullable=False)  # Format: "9:00 AM"
    subject = db.Column(db.String(100), nullable=False)
    teacher = db.Column(db.String(100), nullable=True)
    room = db.Column(db.String(50), nullable=True)
    type = db.Column(db.String(50), nullable=True)  # "lecture", "lab", etc.
    schedule_id = db.Column(db.Integer, db.ForeignKey('schedule.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id',ondelete='CASCADE'), nullable=False)
    institution_id = db.Column(db.Integer, db.ForeignKey('institutions.id', ondelete='CASCADE'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id', ondelete='CASCADE'), nullable=False)
    time_ID = db.Column(db.Integer, db.ForeignKey('time.id', ondelete='CASCADE'), nullable=False)
    __table_args__ = (db.UniqueConstraint('time', 'schedule_id', name='_time_schedule_uc'),)

    def __repr__(self):
        return f'<TimeSlot {self.time}: {self.subject}>'
