from flask import Blueprint, request, jsonify
from App.models.teachers import Teacher 
from App.models import db

teacher_bp = Blueprint('teacher', __name__)

@teacher_bp.route('/teacher/register', methods=['POST'])
def create_teacher():
    data = request.get_json()
    print(data)
    teacher = Teacher(
        full_name=data['full_name'],
        email=data['email'],
        department_id=data['department_id'],
        user_id=data['user_id'],
        institution_id=data["institution_id"],
    )
    db.session.add(teacher)
    db.session.commit()
    return jsonify({'message': 'Teacher created', 'teacher': {
        "id": teacher.id,
        "name": teacher.full_name,
        "email": teacher.email,
        "department_id": teacher.department_id,
        "user_id":teacher.user_id,
        "institution_id": teacher.institution_id,
    }}), 201


@teacher_bp.route('/teacher/<int:id>', methods=['DELETE'])
def delete_teacher(id):
    teacher = Teacher.query.get_or_404(id)
    db.session.delete(teacher)
    db.session.commit()
    return jsonify({'message': 'Teacher deleted'})

@teacher_bp.route('/teacher/<string:inst_id>', methods=['GET'])
def get_all_teachers(inst_id):
    teachers = Teacher.query.filter_by(institution_id=inst_id).all()
    t = []
    for teacher in teachers:
        dept_dict = {
            "id": teacher.id,
            "name": teacher.full_name,
            "email": teacher.email,
            "department_id": teacher.department_id,
            "institution_id": teacher.institution_id
        }
        t.append(dept_dict)
    return jsonify({"teachers": t})

@teacher_bp.route('/teacher/user/<id>', methods=['GET'])
def get_teacher_by_id(id):
    teacher = Teacher.query.filter_by(user_id=id).first()
    dept_dict = {
        "id": teacher.id,
        "name": teacher.full_name,
        "email": teacher.email,
        "department_id": teacher.department_id,
        "institution_id": teacher.institution_id
    }
    return jsonify({"teacher": dept_dict})