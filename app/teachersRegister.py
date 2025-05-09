from flask import Blueprint, request, jsonify
from models.teachers import Teacher 
from models import db

teacher_bp = Blueprint('teacher', __name__)


@teacher_bp.route('/teacher', methods=['POST'])
def create_teacher():
    data = request.json
    teacher = Teacher(
        full_name=data['full_name'],
        email=data['email'],
        department_id=data['department_id'],
        course=data['course']
    )
    db.session.add(teacher)
    db.session.commit()
    return jsonify({'message': 'Teacher created', 'teacher': teacher.to_dict()}), 201

@teacher_bp.route('/teacher/<int:id>', methods=['PUT'])
def update_teacher(id):
    teacher = Teacher.query.get_or_404(id)
    data = request.json
    teacher.full_name = data.get('full_name', teacher.full_name)
    teacher.email = data.get('email', teacher.email)
    teacher.course = data.get('course', teacher.course)
    db.session.commit()
    return jsonify({'message': 'Teacher updated', 'teacher': teacher.to_dict()})

@teacher_bp.route('/teacher/<int:id>', methods=['DELETE'])
def delete_teacher(id):
    teacher = Teacher.query.get_or_404(id)
    db.session.delete(teacher)
    db.session.commit()
    return jsonify({'message': 'Teacher deleted'})

@teacher_bp.route('/teacher', methods=['GET'])
def get_all_teachers():
    teachers = Teacher.query.all()
    return jsonify([t.to_dict() for t in teachers])

@teacher_bp.route('/teacher/<int:id>', methods=['GET'])
def get_teacher(id):
    teacher = Teacher.query.get_or_404(id)
    return jsonify(teacher.to_dict())