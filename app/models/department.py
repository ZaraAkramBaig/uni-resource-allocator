from app import db

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(10), unique=True, nullable=False)
    institution_id = db.Column(db.Integer, db.ForeignKey('institutions.id'), nullable=False)
    
    # # Relationships
    # faculty = db.relationship('Faculty', backref='department', lazy=True)
    # courses = db.relationship('Course', backref='department', lazy=True)
    department_heads = db.relationship('DepartmentHead', backref='department', lazy=True)
    # students = db.relationship('Student', backref='department', lazy=True)