from flask import jsonify
from flask import request, Blueprint
from App.models.admin import Admin
from App.models.university import Institution
from App.models import db
import datetime
import bcrypt

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
        website_url=data.get('website_url'),
        country=data['country'],
        state_province=data['state_province'],
        city=data['city'],
        postal_code=data['postal_code'],
        full_address=data['full_address'],
        accreditation_details=data.get('accreditation_details'),
        additional_notes=data.get('additional_notes'),
        active=False,
        created_at=datetime.datetime.now(),
        admin_full_name=data.get('admin_full_name'),
        admin_phone_number=data.get('admin_phone_number'),
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
            "admin_full_name": institution.admin_full_name,
            "admin_phone_number": institution.admin_phone_number,
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
@institution.route('/institution/<string:id>', methods=['DELETE'])
def delete_institution(id):
    institution = Institution.query.get(id)
    if not institution:
        return jsonify({'error': 'Institution not found'}), 404
    
    # Delete the institution
    db.session.delete(institution)
    db.session.commit()
    
    return jsonify({'message': 'Institution deleted successfully'}), 200



# Register Admin for Institution
@institution.route('/institution/<int:institution_id>/admin/register', methods=['POST'])
def register_admin(institution_id):
    data = request.get_json()
    
    # Check if institution exists
    institution = Institution.query.get(institution_id)
    if not institution:
        return jsonify({'error': 'Institution not found'}), 404
    
    admin = Admin.query.filter_by(institution_id=institution_id).first()
    if admin:
        return jsonify({'error': 'Admin already exists for this institution'}), 400

    password=bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt(10)).decode('utf-8')

    # Create new admin instance
    new_admin = Admin(
        institution_id=institution.id,
        user_id=data['user_id'],
        full_name=data['full_name'],
        email=data['email'],
        phone=data['phone'],
        password=password,
        created_at=datetime.datetime.now()
    )
    

    institution.active = True
    institution.admin = new_admin

    # Add to database
    db.session.add(new_admin)
    db.session.commit()
    
    return jsonify({'message': 'Admin registered successfully'}), 201

