from datetime import datetime
from App.models import db
class Institution(db.Model):
    __tablename__ = 'institutions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    year_established = db.Column(db.Integer)
    institution_code = db.Column(db.String(50), unique=True)

    # Contact Information=
    website_url = db.Column(db.String(255))

    # Location
    country = db.Column(db.String(100), nullable=False)
    state_province = db.Column(db.String(100))
    city = db.Column(db.String(100))
    postal_code = db.Column(db.String(20))
    full_address = db.Column(db.Text)

    admin_full_name = db.Column(db.String(150), nullable=False)
    admin_phone_number = db.Column(db.String(20), nullable=False)

    # Other Info
    accreditation_details = db.Column(db.Text)
    additional_notes = db.Column(db.Text)

    # Relationship with admin
    admin = db.relationship(
    'Admin',
    backref=db.backref('institution', passive_deletes=True),
    uselist=False,
    cascade='all, delete-orphan',
    lazy=True
)
    departments = db.relationship(
    'Department',
    backref=db.backref('institution', lazy=True),
    cascade='all, delete-orphan',
    passive_deletes=True,
    lazy=True
)
    active = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)