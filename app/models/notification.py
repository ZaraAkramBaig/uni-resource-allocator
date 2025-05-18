from datetime import datetime
from App.models import db

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    currentDay = db.Column(db.String(20), nullable=False)
    currentTime = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text, nullable=True)
    preferredDay = db.Column(db.String(20), nullable=True)
    preferredTime = db.Column(db.String(20), nullable=True)
    requestType = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='pending')
    subject = db.Column(db.String(100), nullable=False)
    teacherId = db.Column(db.Integer, nullable=False)
    teacherName = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id',ondelete='CASCADE'), nullable=False)
    institution_id = db.Column(db.Integer, db.ForeignKey('institutions.id', ondelete='CASCADE'), nullable=False)
    response = db.Column(db.Text, nullable=True)
    acknowledgement = db.Column(db.Boolean, default=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'currentDay': self.currentDay,
            'currentTime': self.currentTime,
            'message': self.message,
            'preferredDay': self.preferredDay,
            'preferredTime': self.preferredTime,
            'requestType': self.requestType,
            'status': self.status,
            'subject': self.subject,
            'teacherId': self.teacherId,
            'teacherName': self.teacherName,
            'timestamp': self.timestamp.isoformat(),
            "response": self.response,
            "acknowledgement": self.acknowledgement

        }
