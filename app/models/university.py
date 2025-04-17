from app import db

class University(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    # Relationships
    departments = db.relationship('Department', backref='university', lazy=True)
    admins = db.relationship('User', backref='admin_university', lazy=True,
                           primaryjoin="and_(User.university_id==University.id, User.role=='admin')")
    faculty = db.relationship('User', backref='faculty_university', lazy=True,
                            primaryjoin="and_(User.university_id==University.id, User.role=='faculty')")
    students = db.relationship('User', backref='student_university', lazy=True,
                             primaryjoin="and_(User.university_id==University.id, User.role=='student')")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at)
        }