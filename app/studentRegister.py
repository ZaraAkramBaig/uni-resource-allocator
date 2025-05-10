from flask import Blueprint, request, jsonify
from models.students import Student, Program
from models import db

student_bp = Blueprint('student', __name__)

@student_bp.route('/student', methods=['POST'])
def create_student():
    data = request.json
    student = Student(
        full_name=data['full_name'],
        email=data['email'],
        password=data['password'],
        department_id=data['department_id'],
        program_id=data['program_id']
    )
    db.session.add(student)
    db.session.commit()
    return jsonify({'message': 'Student created', 'student': student.to_dict()}), 201

@student_bp.route('/student/<int:id>', methods=['PUT'])
def update_student(id):
    student = Student.query.get_or_404(id)
    data = request.json
    student.full_name = data.get('full_name', student.full_name)
    student.email = data.get('email', student.email)
    student.password = data.get('password', student.password)
    student.department_id = data.get('department_id', student.department_id)
    student.program_id = data.get('program_id', student.program_id)
    db.session.commit()
    return jsonify({'message': 'Student updated', 'student': student.to_dict()})

@student_bp.route('/student/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return jsonify({'message': 'Student deleted'})

@student_bp.route('/student', methods=['GET'])
def get_all_students():
    students = Student.query.all()
    return jsonify([s.to_dict() for s in students])

@student_bp.route('/student/<int:id>', methods=['GET'])
def get_student(id):
    student = Student.query.get_or_404(id)
    return jsonify(student.to_dict())


# from flask import Blueprint, request, jsonify
# from models.students import Student, Program
# from models import db

# student_bp = Blueprint('student', __name__)

# @student_bp.route('/student', methods=['POST'])
# def create_student():
#     data = request.json

#     # Optional: validate program_id exists
#     program = Program.query.get(data['program_id'])
#     if not program:
#         return jsonify({'error': 'Program not found'}), 404

#     student = Student(
#         full_name=data['full_name'],
#         email=data['email'],
#         password=data['password'],
#         department_id=data['department_id'],
#         program_id=data['program_id']
#     )
#     db.session.add(student)
#     db.session.commit()
#     return jsonify({'message': 'Student created', 'student': student_to_dict(student)}), 201


# @student_bp.route('/student/<int:id>', methods=['PUT'])
# def update_student(id):
#     student = Student.query.get_or_404(id)
#     data = request.json

#     student.full_name = data.get('full_name', student.full_name)
#     student.email = data.get('email', student.email)
#     student.password = data.get('password', student.password)
    
#     # If updating program_id
#     if 'program_id' in data:
#         program = Program.query.get(data['program_id'])
#         if not program:
#             return jsonify({'error': 'Program not found'}), 404
#         student.program_id = data['program_id']

#     db.session.commit()
#     return jsonify({'message': 'Student updated', 'student': student_to_dict(student)})


# @student_bp.route('/student/<int:id>', methods=['DELETE'])
# def delete_student(id):
#     student = Student.query.get_or_404(id)
#     db.session.delete(student)
#     db.session.commit()
#     return jsonify({'message': 'Student deleted'})


# @student_bp.route('/student', methods=['GET'])
# def get_all_students():
#     students = Student.query.all()
#     return jsonify([student_to_dict(s) for s in students])


# @student_bp.route('/student/<int:id>', methods=['GET'])
# def get_student(id):
#     student = Student.query.get_or_404(id)
#     return jsonify(student_to_dict(student))


# # 🧠 Helper function to safely serialize student + program
# def student_to_dict(student):
#     return {
#         'id': student.id,
#         'full_name': student.full_name,
#         'email': student.email,
#         'department_id': student.department_id,
#         'program_id': student.program_id,
#     }


# # from flask import Blueprint, request, jsonify
# # from models.students import Student
# # from models import db

# # student_bp = Blueprint('student', __name__)


# # @student_bp.route('/student', methods=['POST'])
# # def create_student():
# #     data = request.json
# #     student = Student(
# #         full_name=data['full_name'],
# #         email=data['email'],
# #         password=data['password'],
# #         department_id=data['department_id'],
# #         program=data['program']
# #     )
# #     db.session.add(student)
# #     db.session.commit()
# #     return jsonify({'message': 'Student created', 'student': student.to_dict()}), 201

# # @student_bp.route('/student/<int:id>', methods=['PUT'])
# # def update_student(id):
# #     student = Student.query.get_or_404(id)
# #     data = request.json
# #     student.full_name = data.get('full_name', student.full_name)
# #     student.email = data.get('email', student.email)
# #     student.password = data.get('password', student.password)
# #     student.program = data.get('program', student.program)
# #     db.session.commit()
# #     return jsonify({'message': 'Student updated', 'student': student.to_dict()})

# # @student_bp.route('/student/<int:id>', methods=['DELETE'])
# # def delete_student(id):
# #     student = Student.query.get_or_404(id)
# #     db.session.delete(student)
# #     db.session.commit()
# #     return jsonify({'message': 'Student deleted'})


# # @student_bp.route('/student', methods=['GET'])
# # def get_all_students():
# #     students = Student.query.all()
# #     return jsonify([s.to_dict() for s in students])

# # @student_bp.route('/student/<int:id>', methods=['GET'])
# # def get_student(id):
# #     student = Student.query.get_or_404(id)
# #     return jsonify(student.to_dict())