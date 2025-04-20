from flask import jsonify
from flask import request, flash, Blueprint
from .models.SuperAdmin import Admin
from .models.university import Institution
from App.models import db

institution = Blueprint('institution', __name__)

@institution.route('/institution/register', methods=['POST'])
def register_institution():
    data = request.get_json()
    
    # Validate input data
    required_fields = ['name', 'institution_type', 'year_established', 'institution_code',
                       'official_email', 'phone_number', 'country', 'state_province',
                       'city', 'postal_code', 'full_address']
    
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400
    
    # Create new institution instance
    new_institution = Institution(
        name=data['name'],
        institution_type=data['institution_type'],
        year_established=data['year_established'],
        institution_code=data['institution_code'],
        official_email=data['official_email'],
        phone_number=data['phone_number'],
        alternate_phone=data.get('alternate_phone'),
        website_url=data.get('website_url'),
        country=data['country'],
        state_province=data['state_province'],
        city=data['city'],
        postal_code=data['postal_code'],
        full_address=data['full_address'],
        num_departments=data.get('num_departments'),
        num_students_faculty=data.get('num_students_faculty'),
        accreditation_details=data.get('accreditation_details'),
        additional_notes=data.get('additional_notes')
    )
    
    # Add to database
    db.session.add(new_institution)
    db.session.commit()
    
    return jsonify({'message': 'Institution registered successfully'}), 201

#Get Institutions
@institution.route('/institution', methods=['GET'])
def get_institutions():
    institutions = Institution.query.all()
    institution_list = []
    
    for institution in institutions:
        institution_data = {
            'id': institution.id,
            'name': institution.name,
            'institution_type': institution.institution_type,
            'year_established': institution.year_established,
            'institution_code': institution.institution_code,
            'official_email': institution.official_email,
            'phone_number': institution.phone_number,
            'alternate_phone': institution.alternate_phone,
            'website_url': institution.website_url,
            'country': institution.country,
            'state_province': institution.state_province,
            'city': institution.city,
            'postal_code': institution.postal_code,
            'full_address': institution.full_address,
            'num_departments': institution.num_departments,
            'num_students_faculty': institution.num_students_faculty,
            'accreditation_details': institution.accreditation_details,
            'additional_notes': institution.additional_notes
        }
        institution_list.append(institution_data)
    
    return jsonify(institution_list), 200

# Register Admin for Institution
@institution.route('/institution/<int:institution_id>/admin/register', methods=['POST'])
def register_admin(institution_id):
    data = request.get_json()
    
    # Validate input data
    required_fields = ['full_name', 'email', 'phone', 'password_hash']
    
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400
    
    # Check if institution exists
    institution = Institution.query.get(institution_id)
    if not institution:
        return jsonify({'error': 'Institution not found'}), 404
    
    # Create new admin instance
    new_admin = Admin(
        institution_id=institution.id,
        full_name=data['full_name'],
        email=data['email'],
        phone=data['phone'],
        password_hash=data['password_hash']
    )
    
    # Add to database
    db.session.add(new_admin)
    db.session.commit()
    
    return jsonify({'message': 'Admin registered successfully'}), 201