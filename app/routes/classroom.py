# from flask import Blueprint, jsonify, request
# from app.models.classroom import Classroom
# from app import db

# bp = Blueprint('classrooms', __name__)

# @bp.route('/', methods=['GET'])
# def get_classrooms():
#     classrooms = Classroom.query.all()
#     return jsonify([classroom.to_dict() for classroom in classrooms])

# @bp.route('/<int:id>', methods=['GET'])
# def get_classroom(id):
#     classroom = Classroom.query.get_or_404(id)
#     return jsonify(classroom.to_dict())

# @bp.route('/', methods=['POST'])
# def create_classroom():
#     data = request.get_json()
    
#     if not data or not data.get('room_number') or not data.get('capacity'):
#         return jsonify({'error': 'Missing required fields'}), 400
        
#     classroom = Classroom(
#         room_number=data['room_number'],
#         capacity=data['capacity'],
#         is_lab=data.get('is_lab', False)
#     )
    
#     db.session.add(classroom)
#     db.session.commit()
    
#     return jsonify(classroom.to_dict()), 201

# @bp.route('/<int:id>', methods=['PUT'])
# def update_classroom(id):
#     classroom = Classroom.query.get_or_404(id)
#     data = request.get_json()
    
#     if 'room_number' in data:
#         classroom.room_number = data['room_number']
#     if 'capacity' in data:
#         classroom.capacity = data['capacity']
#     if 'is_lab' in data:
#         classroom.is_lab = data['is_lab']
    
#     db.session.commit()
#     return jsonify(classroom.to_dict())

# @bp.route('/<int:id>', methods=['DELETE'])
# def delete_classroom(id):
#     classroom = Classroom.query.get_or_404(id)
#     db.session.delete(classroom)
#     db.session.commit()
#     return '', 204

from flask import Blueprint, jsonify, request
from app.models.classroom import Classroom
from app.schemas import ClassroomSchema
from app.auth import admin_required, faculty_required
from app import db
import logging

bp = Blueprint('classrooms', __name__)
logger = logging.getLogger(__name__)
classroom_schema = ClassroomSchema()
classrooms_schema = ClassroomSchema(many=True)

@bp.route('/', methods=['GET'])
@faculty_required()
def get_classrooms():
    classrooms = Classroom.query.all()
    logger.info(f"Retrieved {len(classrooms)} classrooms")
    return jsonify(classrooms_schema.dump(classrooms))

@bp.route('/<int:id>', methods=['GET'])
@faculty_required()
def get_classroom(id):
    classroom = Classroom.query.get_or_404(id)
    logger.info(f"Retrieved classroom {id}")
    return jsonify(classroom_schema.dump(classroom))

@bp.route('/', methods=['POST'])
@admin_required()
def create_classroom():
    data = classroom_schema.load(request.get_json())
    classroom = Classroom(**data)
    
    db.session.add(classroom)
    db.session.commit()
    
    logger.info(f"Created new classroom: {classroom.room_number}")
    return jsonify(classroom_schema.dump(classroom)), 201

@bp.route('/<int:id>', methods=['PUT'])
@admin_required()
def update_classroom(id):
    classroom = Classroom.query.get_or_404(id)
    data = classroom_schema.load(request.get_json(), partial=True)
    
    for key, value in data.items():
        setattr(classroom, key, value)
    
    db.session.commit()
    logger.info(f"Updated classroom {id}")
    return jsonify(classroom_schema.dump(classroom))

@bp.route('/<int:id>', methods=['DELETE'])
@admin_required()
def delete_classroom(id):
    classroom = Classroom.query.get_or_404(id)
    db.session.delete(classroom)
    db.session.commit()
    logger.info(f"Deleted classroom {id}")
    return '', 204
