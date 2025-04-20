from datetime import datetime
from .SuperAdmin import Admin  # Assuming Admin model is in the same directory
from App.models import db
class Institution(db.Model):
    __tablename__ = 'institutions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    institution_type = db.Column(db.String(50), nullable=False)  # University, College, Institute, etc.
    year_established = db.Column(db.Integer)
    institution_code = db.Column(db.String(50), unique=True)

    # Contact Information
    official_email = db.Column(db.String(120), nullable=False, unique=True)
    phone_number = db.Column(db.String(20), nullable=False)
    alternate_phone = db.Column(db.String(20))
    website_url = db.Column(db.String(255))

    # Location
    country = db.Column(db.String(100), nullable=False)
    state_province = db.Column(db.String(100))
    city = db.Column(db.String(100))
    postal_code = db.Column(db.String(20))
    full_address = db.Column(db.Text)

    # Other Info
    num_departments = db.Column(db.Integer)
    num_students_faculty = db.Column(db.Integer)
    accreditation_details = db.Column(db.Text)
    additional_notes = db.Column(db.Text)

    # Relationship with admin
    admin = db.relationship('Admin', backref='institution', uselist=False, cascade="all, delete", lazy=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)