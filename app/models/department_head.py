from app import db
from datetime import datetime
import uuid

class DepartmentHead(db.Model):
    __tablename__ = 'DepartmentHead'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    institution_id = db.Column(db.Integer, db.ForeignKey('institutions.id', ondelete="CASCADE"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    department_id=  db.Column(db.Integer, db.ForeignKey('department.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)



