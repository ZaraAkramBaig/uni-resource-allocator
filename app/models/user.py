from App.models import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'super_admin', 'admin', 'faculty', 'student'
    institution_id = db.Column(db.Integer, db.ForeignKey('institutions.id', ondelete='CASCADE'))
    department_id = db.Column(db.Integer, db.ForeignKey('department.id', ondelete='CASCADE'))
    
    

