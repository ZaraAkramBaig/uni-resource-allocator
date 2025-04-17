# from flask import Blueprint, jsonify, request
# from app.models.student import Student
# from app import db

# bp = Blueprint('students', __name__)

# @bp.route('/', methods=['GET'])
# def get_students():
#     students = Student.query.all()
#     return jsonify([student.to_dict() for student in students])

# @bp.route('/<int:id>', methods=['GET'])
# def get_student(id):
#     student = Student.query.get_or_404(id)
#     return jsonify(student.to_dict())

# @bp.route('/', methods=['POST'])
# def create_student():
#     data = request.get_json()
    
#     required_fields = ['name', 'email', 'student_id']
#     if not all(field in data for field in required_fields):
#         return jsonify({'error': 'Missing required fields'}), 400
        
#     student = Student(
#         name=data['name'],
#         email=data['email'],
#         student_id=data['student_id']
#     )
    
#     db.session.add(student)
#     db.session.commit()
    
#     return jsonify(student.to_dict()), 201

# @bp.route('/<int:id>', methods=['PUT'])
# def update_student(id):
#     student = Student.query.get_or_404(id)
#     data = request.get_json()
    
#     if 'name' in data:
#         student.name = data['name']
#     if 'email' in data:
#         student.email = data['email']
#     if 'student_id' in data:
#         student.student_id = data['student_id']
    
#     db.session.commit()
#     return jsonify(student.to_dict())

# @bp.route('/<int:id>', methods=['DELETE'])
# def delete_student(id):
#     student = Student.query.get_or_404(id)
#     db.session.delete(student)
#     db.session.commit()
#     return '', 204

from flask import Blueprint, jsonify, request
from app.models.student import Student
from app.schemas import StudentSchema
from app.auth import admin_required, faculty_required, student_required
from app import db
import logging

bp = Blueprint('students', __name__)
logger = logging.getLogger(__name__)
student_schema = StudentSchema()
students_schema = StudentSchema(many=True)

@bp.route('/', methods=['GET'])
@faculty_required()
def get_students():
    students = Student.query.all()
    logger.info(f"Retrieved {len(students)} students")
    return jsonify(students_schema.dump(students))

@bp.route('/<int:id>', methods=['GET'])
@student_required()
def get_student(id):
    student = Student.query.get_or_404(id)
    logger.info(f"Retrieved student {id}")
    return jsonify(student_schema.dump(student))

@bp.route('/', methods=['POST'])
@admin_required()
def create_student():
    data = student_schema.load(request.get_json())
    student = Student(**data)
    
    db.session.add(student)
    db.session.commit()
    
    logger.info(f"Created new student: {student.name}")
    return jsonify(student_schema.dump(student)), 201

@bp.route('/<int:id>', methods=['PUT'])
@admin_required()
def update_student(id):
    student = Student.query.get_or_404(id)
    data = student_schema.load(request.get_json(), partial=True)
    
    for key, value in data.items():
        setattr(student, key, value)
    
    db.session.commit()
    logger.info(f"Updated student {id}")
    return jsonify(student_schema.dump(student))

@bp.route('/<int:id>', methods=['DELETE'])
@admin_required()
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    logger.info(f"Deleted student {id}")
    return '', 204