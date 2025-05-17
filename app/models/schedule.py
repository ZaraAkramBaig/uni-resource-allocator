from App.models import db

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(10), nullable=False)  # "Monday", "Tuesday", etc.
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'), nullable=False)
    slots = db.relationship('TimeSlot', backref='schedule', cascade='all, delete-orphan')

    __table_args__ = (db.UniqueConstraint('day', 'section_id', name='_day_section_uc'),)

    def __repr__(self):
        return f'<Schedule for {self.day} of {self.section.name}>'