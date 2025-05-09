
from models.resources import Classroom
from flask import Blueprint, request, jsonify
from models import db

resources_bp = Blueprint('resources', __name__)


@resources_bp.route('/classroom', methods=['POST'])
def create_classroom():
    data = request.json
    classroom = Classroom(
        room_number=data['room_number'],
        department_id=data['department_id'],
        capacity=data['capacity'],
        time_slot=data.get('time_slot')
    )
    db.session.add(classroom)
    db.session.commit()
    return jsonify({'message': 'Classroom created', 'classroom': classroom.to_dict()}), 201

@resources_bp.route('/classroom/<int:id>', methods=['PUT'])
def update_classroom(id):
    classroom = Classroom.query.get_or_404(id)
    data = request.json
    classroom.room_number = data.get('room_number', classroom.room_number)
    classroom.capacity = data.get('capacity', classroom.capacity)
    classroom.time_slot = data.get('time_slot', classroom.time_slot)
    db.session.commit()
    return jsonify({'message': 'Classroom updated', 'classroom': classroom.to_dict()})

@resources_bp.route('/classroom/<int:id>', methods=['DELETE'])
def delete_classroom(id):
    classroom = Classroom.query.get_or_404(id)
    db.session.delete(classroom)
    db.session.commit()
    return jsonify({'message': 'Classroom deleted'})

@resources_bp.route('/classroom', methods=['GET'])
def get_all_classrooms():
    classrooms = Classroom.query.all()
    return jsonify([c.to_dict() for c in classrooms])

@resources_bp.route('/classroom/<int:id>', methods=['GET'])
def get_classroom(id):
    classroom = Classroom.query.get_or_404(id)
    return jsonify(classroom.to_dict())