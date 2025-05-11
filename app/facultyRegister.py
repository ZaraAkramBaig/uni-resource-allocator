from flask import Blueprint, request, jsonify
from models.faculty import Faculty
from models import db

faculty_bp = Blueprint('faculty', __name__)

@faculty_bp.route('/faculty', methods=['POST'])
def create_faculty():
    data = request.json
    faculty = Faculty(
        name=data['name'],
        email=data['email'],
        department_id=data['department_id']
    )
    db.session.add(faculty)
    db.session.commit()
    return jsonify({'message': 'Faculty created', 'faculty': faculty.to_dict()}), 201

@faculty_bp.route('/faculty/<int:id>', methods=['PUT'])
def update_faculty(id):
    faculty = Faculty.query.get_or_404(id)
    data = request.json
    faculty.name = data.get('name', faculty.name)
    faculty.email = data.get('email', faculty.email)
    faculty.department_id = data.get('department_id', faculty.department_id)
    db.session.commit()
    return jsonify({'message': 'Faculty updated', 'faculty': faculty.to_dict()})

@faculty_bp.route('/faculty/<int:id>', methods=['DELETE'])
def delete_faculty(id):
    faculty = Faculty.query.get_or_404(id)
    db.session.delete(faculty)
    db.session.commit()
    return jsonify({'message': 'Faculty deleted'})

@faculty_bp.route('/faculty', methods=['GET'])
def get_all_faculty():
    faculty_list = Faculty.query.all()
    return jsonify([f.to_dict() for f in faculty_list])

@faculty_bp.route('/faculty/<int:id>', methods=['GET'])
def get_faculty(id):
    faculty = Faculty.query.get_or_404(id)
    return jsonify(faculty.to_dict())


# from flask import Blueprint, request, jsonify
# from models.teachers import Teacher 
# from models import db

# teacher_bp = Blueprint('teacher', __name__)


# @teacher_bp.route('/teacher', methods=['POST'])
# def create_teacher():
#     data = request.json
#     teacher = Teacher(
#         full_name=data['full_name'],
#         email=data['email'],
#         department_id=data['department_id'],
#         course=data['course']
#     )
#     db.session.add(teacher)
#     db.session.commit()
#     return jsonify({'message': 'Teacher created', 'teacher': teacher.to_dict()}), 201

# @teacher_bp.route('/teacher/<int:id>', methods=['PUT'])
# def update_teacher(id):
#     teacher = Teacher.query.get_or_404(id)
#     data = request.json
#     teacher.full_name = data.get('full_name', teacher.full_name)
#     teacher.email = data.get('email', teacher.email)
#     teacher.course = data.get('course', teacher.course)
#     db.session.commit()
#     return jsonify({'message': 'Teacher updated', 'teacher': teacher.to_dict()})

# @teacher_bp.route('/teacher/<int:id>', methods=['DELETE'])
# def delete_teacher(id):
#     teacher = Teacher.query.get_or_404(id)
#     db.session.delete(teacher)
#     db.session.commit()
#     return jsonify({'message': 'Teacher deleted'})

# @teacher_bp.route('/teacher', methods=['GET'])
# def get_all_teachers():
#     teachers = Teacher.query.all()
#     return jsonify([t.to_dict() for t in teachers])

# @teacher_bp.route('/teacher/<int:id>', methods=['GET'])
# def get_teacher(id):
#     teacher = Teacher.query.get_or_404(id)
#     return jsonify(teacher.to_dict())