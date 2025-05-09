from datetime import datetime
from App.models import db

class Admin(db.Model):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    institution_id = db.Column(db.Integer, db.ForeignKey('institutions.id', ondelete='CASCADE'), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    password = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
