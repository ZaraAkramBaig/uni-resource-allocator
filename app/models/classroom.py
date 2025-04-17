from app import db

class Classroom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(20), unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    is_lab = db.Column(db.Boolean, default=False)
    
    # Relationships
    courses = db.relationship('Course', backref='classroom', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'room_number': self.room_number,
            'capacity': self.capacity,
            'is_lab': self.is_lab
        }