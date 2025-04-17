# from flask import Blueprint, jsonify, request
# from app.models.department import Department
# from app import db

# bp = Blueprint('departments', __name__)

# @bp.route('/', methods=['GET'])
# def get_departments():
#     departments = Department.query.all()
#     return jsonify([dept.to_dict() for dept in departments])

# @bp.route('/<int:id>', methods=['GET'])
# def get_department(id):
#     department = Department.query.get_or_404(id)
#     return jsonify(department.to_dict())

# @bp.route('/', methods=['POST'])
# def create_department():
#     data = request.get_json()
    
#     if not data or not data.get('name') or not data.get('code'):
#         return jsonify({'error': 'Missing required fields'}), 400
        
#     department = Department(
#         name=data['name'],
#         code=data['code']
#     )
    
#     db.session.add(department)
#     db.session.commit()
    
#     return jsonify(department.to_dict()), 201

from flask import Blueprint, jsonify, request
from app.models.department import Department
from app.schemas import DepartmentSchema
from app.auth import admin_required, faculty_required
from app import db
import logging

bp = Blueprint('departments', __name__)
logger = logging.getLogger(__name__)
department_schema = DepartmentSchema()
departments_schema = DepartmentSchema(many=True)

@bp.route('/', methods=['GET'])
@faculty_required()
def get_departments():
    departments = Department.query.all()
    logger.info(f"Retrieved {len(departments)} departments")
    return jsonify(departments_schema.dump(departments))

@bp.route('/<int:id>', methods=['GET'])
@faculty_required()
def get_department(id):
    department = Department.query.get_or_404(id)
    logger.info(f"Retrieved department {id}")
    return jsonify(department_schema.dump(department))

@bp.route('/', methods=['POST'])
@admin_required()
def create_department():
    data = department_schema.load(request.get_json())
    department = Department(**data)
    
    db.session.add(department)
    db.session.commit()
    
    logger.info(f"Created new department: {department.name}")
    return jsonify(department_schema.dump(department)), 201

@bp.route('/<int:id>', methods=['PUT'])
@admin_required()
def update_department(id):
    department = Department.query.get_or_404(id)
    data = department_schema.load(request.get_json(), partial=True)
    
    for key, value in data.items():
        setattr(department, key, value)
    
    db.session.commit()
    logger.info(f"Updated department {id}")
    return jsonify(department_schema.dump(department))

@bp.route('/<int:id>', methods=['DELETE'])
@admin_required()
def delete_department(id):
    department = Department.query.get_or_404(id)
    db.session.delete(department)
    db.session.commit()
    logger.info(f"Deleted department {id}")
    return '', 204