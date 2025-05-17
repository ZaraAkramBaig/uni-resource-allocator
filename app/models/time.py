from App.models import db

class Time(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(20), nullable=False)  # Format: "9:00 AM"
    department_id = db.Column(db.Integer, db.ForeignKey('department.id',ondelete='CASCADE'), nullable=False)
    institution_id = db.Column(db.Integer, db.ForeignKey('institutions.id', ondelete='CASCADE'), nullable=False)
    
    def __repr__(self):
        return f'<TimeSlot {self.time}: {self.subject}>'