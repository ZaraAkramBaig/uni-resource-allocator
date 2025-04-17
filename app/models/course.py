from app import db

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'))
    classroom_id = db.Column(db.Integer, db.ForeignKey('classroom.id'))
    schedule_day = db.Column(db.String(10))  # Monday, Tuesday, etc.
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    
    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'department_id': self.department_id,
            'faculty_id': self.faculty_id,
            'classroom_id': self.classroom_id,
            'schedule_day': self.schedule_day,
            'start_time': str(self.start_time) if self.start_time else None,
            'end_time': str(self.end_time) if self.end_time else None
        }