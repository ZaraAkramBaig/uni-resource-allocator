# from models import db

# class Teacher(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     full_name = db.Column(db.String(100), nullable=False)
#     email = db.Column(db.String(100), unique=True, nullable=False)
#     department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
#     course = db.Column(db.String(100), nullable=False)
