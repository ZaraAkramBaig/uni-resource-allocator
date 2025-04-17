# from app import db
# from werkzeug.security import generate_password_hash, check_password_hash

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password_hash = db.Column(db.String(256), nullable=False)
#     role = db.Column(db.String(20), nullable=False)  # 'admin', 'faculty', 'student'
    
#     # Link to either Student or Faculty based on role
#     student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
#     faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'))
    
#     def set_password(self, password):
#         self.password_hash = generate_password_hash(password)
        
#     def check_password(self, password):
#         return check_password_hash(self.password_hash, password)
        
#     def to_dict(self):
#         return {
#             'id': self.id,
#             'username': self.username,
#             'email': self.email,
#             'role': self.role
#         }

from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'super_admin', 'admin', 'faculty', 'student'
    university_id = db.Column(db.Integer, db.ForeignKey('university.id'))
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    # Relationships
    department = db.relationship('Department', backref='users')
    courses_teaching = db.relationship('Course', backref='instructor', lazy=True)
    notifications = db.relationship('Notification', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'role': self.role,
            'university_id': self.university_id,
            'department_id': self.department_id,
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at)
        }