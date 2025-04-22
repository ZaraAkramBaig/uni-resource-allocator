from flask import jsonify
from flask import request, flash, Blueprint
from .models.SuperAdmin import Admin
from .models.university import Institution
from App.models import db
import datetime

institution = Blueprint('institution', __name__)

@institution.route('/institution/register', methods=['POST'])
def register_institution():
    data = request.get_json()
    print(data)
    
    if data['year_established'] == "":
        data['year_established'] = None
    # Create new institution instance
    new_institution = Institution(
        name=data['name'],
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
        accreditation_details=data.get('accreditation_details'),
        additional_notes=data.get('additional_notes'),
        active=False,
        created_at=datetime.datetime.now()
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
            'year_established': int(institution.year_established) if institution.year_established else 0,
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
            'accreditation_details': institution.accreditation_details,
            'additional_notes': institution.additional_notes,
            "active": institution.active,
            "created_at": institution.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "admin": {
                'id': institution.admin.id if institution.admin else None,
                'full_name': institution.admin.full_name if institution.admin else None,
                'email': institution.admin.email if institution.admin else None,
                'phone': institution.admin.phone if institution.admin else None,
                'created_at': institution.admin.created_at.strftime('%Y-%m-%d %H:%M:%S') if institution.admin else None
            } if institution.admin else None
        }
        institution_list.append(institution_data)

    return jsonify(institution_list), 200


#delete institution
@institution.route('/institution/<int:id>', methods=['DELETE'])
def delete_institution(id):
    institution = Institution.query.get(id)
    if not institution:
        return jsonify({'error': 'Institution not found'}), 404
    print(id)
    
    # Delete the institution
    db.session.delete(institution)
    db.session.commit()
    
    return jsonify({'message': 'Institution deleted successfully'}), 200

# Approve Institution
@institution.route('/institution/<int:id>/approve', methods=['PUT'])
def approve_institution(id):
    data=request.get_json()
    institution = Institution.query.get(id)
    print(institution)

    admin = Admin.query.filter_by(institution_id=id).first()
    if not admin:
        return jsonify({'error': 'Admin not found for this institution'}), 404
    
    if not institution:
        return jsonify({'error': 'Institution not found'}), 404
    
    # Approve the institution
    institution.active = data["active"]
    institution.admin = admin
    db.session.commit()
    
    return jsonify({'message': 'Institution approved successfully'}), 200



# Register Admin for Institution
@institution.route('/institution/<int:institution_id>/admin/register', methods=['POST'])
def register_admin(institution_id):
    data = request.get_json()
    
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
        password=data['password'],
        created_at=datetime.datetime.now()
    )
    
    # Add to database
    db.session.add(new_admin)
    db.session.commit()
    
    return jsonify({'message': 'Admin registered successfully'}), 201