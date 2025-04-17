# from flask import Blueprint, jsonify, request
# from app.models.faculty import Faculty
# from app import db

# bp = Blueprint('faculty', __name__)

# @bp.route('/', methods=['GET'])
# def get_faculty_members():
#     faculty = Faculty.query.all()
#     return jsonify([f.to_dict() for f in faculty])

# @bp.route('/<int:id>', methods=['GET'])
# def get_faculty(id):
#     faculty = Faculty.query.get_or_404(id)
#     return jsonify(faculty.to_dict())

# @bp.route('/', methods=['POST'])
# def create_faculty():
#     data = request.get_json()
    
#     required_fields = ['name', 'email', 'department_id']
#     if not all(field in data for field in required_fields):
#         return jsonify({'error': 'Missing required fields'}), 400
        
#     faculty = Faculty(
#         name=data['name'],
#         email=data['email'],
#         department_id=data['department_id']
#     )
    
#     db.session.add(faculty)
#     db.session.commit()
    
#     return jsonify(faculty.to_dict()), 201

# @bp.route('/<int:id>', methods=['PUT'])
# def update_faculty(id):
#     faculty = Faculty.query.get_or_404(id)
#     data = request.get_json()
    
#     if 'name' in data:
#         faculty.name = data['name']
#     if 'email' in data:
#         faculty.email = data['email']
#     if 'department_id' in data:
#         faculty.department_id = data['department_id']
    
#     db.session.commit()
#     return jsonify(faculty.to_dict())

# @bp.route('/<int:id>', methods=['DELETE'])
# def delete_faculty(id):
#     faculty = Faculty.query.get_or_404(id)
#     db.session.delete(faculty)
#     db.session.commit()
#     return '', 204

# @bp.route('/<int:id>/courses', methods=['GET'])
# def get_faculty_courses(id):
#     faculty = Faculty.query.get_or_404(id)
#     return jsonify([course.to_dict() for course in faculty.courses])

from flask import Blueprint, jsonify, request
from app.models.faculty import Faculty
from app.schemas import FacultySchema
from app.auth import admin_required, faculty_required
from app import db
import logging

bp = Blueprint('faculty', __name__)
logger = logging.getLogger(__name__)
faculty_schema = FacultySchema()
faculties_schema = FacultySchema(many=True)

@bp.route('/', methods=['GET'])
@faculty_required()
def get_faculty_members():
    faculty = Faculty.query.all()
    logger.info(f"Retrieved {len(faculty)} faculty members")
    return jsonify(faculties_schema.dump(faculty))

@bp.route('/<int:id>', methods=['GET'])
@faculty_required()
def get_faculty(id):
    faculty = Faculty.query.get_or_404(id)
    logger.info(f"Retrieved faculty member {id}")
    return jsonify(faculty_schema.dump(faculty))

@bp.route('/', methods=['POST'])
@admin_required()
def create_faculty():
    data = faculty_schema.load(request.get_json())
    faculty = Faculty(**data)
    
    db.session.add(faculty)
    db.session.commit()
    
    logger.info(f"Created new faculty member: {faculty.name}")
    return jsonify(faculty_schema.dump(faculty)), 201

@bp.route('/<int:id>', methods=['PUT'])
@admin_required()
def update_faculty(id):
    faculty = Faculty.query.get_or_404(id)
    data = faculty_schema.load(request.get_json(), partial=True)
    
    for key, value in data.items():
        setattr(faculty, key, value)
    
    db.session.commit()
    logger.info(f"Updated faculty member {id}")
    return jsonify(faculty_schema.dump(faculty))

@bp.route('/<int:id>', methods=['DELETE'])
@admin_required()
def delete_faculty(id):
    faculty = Faculty.query.get_or_404(id)
    db.session.delete(faculty)
    db.session.commit()
    logger.info(f"Deleted faculty member {id}")
    return '', 204

@bp.route('/<int:id>/courses', methods=['GET'])
@faculty_required()
def get_faculty_courses(id):
    faculty = Faculty.query.get_or_404(id)
    logger.info(f"Retrieved courses for faculty member {id}")
    return jsonify([course.to_dict() for course in faculty.courses])