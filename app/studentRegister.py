from flask import Blueprint, request, jsonify
from App.models.students import Student
from App.models import db

student_bp = Blueprint('student', __name__)

@student_bp.route('/student', methods=['POST'])
def create_student():
    data = request.get_json()
    student = Student(
        full_name=data['full_name'],
        email=data['email'],
        department_id=data['department_id'],
        institution_id= data["institution_id"],
        user_id=data["user_id"],
        section=data["section"],
        year=data["year"]
    )
    db.session.add(student)
    db.session.commit()
    return jsonify({'message': 'Student created', "studentData":  {
        "id": student.id,
            "name": student.full_name,
            "email": student.email,
            "department_id": student.department_id,
            "institution_id": student.institution_id,
            "section": student.section,
            "year": student.year,
            "user_id": student.user_id
    }}), 201


@student_bp.route('/student/<string:id>', methods=['DELETE'])
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return jsonify({'message': 'Student deleted'})


@student_bp.route('/student/<string:inst_id>', methods=['GET'])
def get_all_students(inst_id):
    students = Student.query.filter_by(institution_id=inst_id).all()
    s = []
    for student in students:
        dept_dict = {
            "id": student.id,
            "name": student.full_name,
            "email": student.email,
            "department_id": student.department_id,
            "institution_id": student.institution_id,
            "section": student.section,
            "year": student.year,
            "user_id": student.user_id

        }
        s.append(dept_dict)
    return jsonify({"students": s})

@student_bp.route('/student/user/<id>', methods=['GET'])
def get_student(id):
    student = Student.query.filter_by(user_id=id).first()
    dept_dict = {
        "id": student.id,
        "name": student.full_name,
        "email": student.email,
        "department_id": student.department_id,
        "institution_id": student.institution_id,
        "section": student.section,
        "year": student.year,
        "user_id": student.user_id

    }
    return jsonify({"student": dept_dict})

