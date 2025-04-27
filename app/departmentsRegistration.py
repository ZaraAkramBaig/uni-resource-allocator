from flask import Blueprint, jsonify, request
from .models import db
from .models.department import Department
from .models.department_head import DepartmentHead
from datetime import datetime

departmentInfo = Blueprint("department", __name__)

# Create Department Head
@departmentInfo.route('/departmentheads/register', methods=['POST'])
def create_department_head():
    data = request.get_json()

    # Validation
    if not all(k in data for k in ("name", "email", "department_id")):
        return jsonify({"error": "Missing required fields"}), 400
    if DepartmentHead.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already exists"}), 400

    new_department_head = DepartmentHead(
        name=data["name"],
        email=data["email"],
        phone_number=data.get("phone_number"),
        department_id=data["department_id"]
    )
    db.session.add(new_department_head)
    db.session.commit()

    return jsonify(new_department_head.to_dict()), 201

# Update Department Head
@departmentInfo.route('/departmentheads/<string:dept_head_id>', methods=['PUT'])
def update_department_head(dept_head_id):
    department_head = DepartmentHead.query.get(dept_head_id)
    if not department_head:
        return jsonify({"error": "Department head not found"}), 404

    data = request.get_json()

    if "name" in data:
        department_head.name = data["name"]
    if "email" in data:
        if DepartmentHead.query.filter(DepartmentHead.email == data["email"], DepartmentHead.id != dept_head_id).first():
            return jsonify({"error": "Email already exists"}), 400
        department_head.email = data["email"]
    if "phone_number" in data:
        department_head.phone_number = data["phone_number"]
    if "department_id" in data:
        department_head.department_id = data["department_id"]

    department_head.updated_at = datetime.utcnow()
    db.session.commit()

    return jsonify(department_head.to_dict()), 200

# Delete Department Head
@departmentInfo.route('/departmentheads/<string:dept_head_id>', methods=['DELETE'])
def delete_department_head(dept_head_id):
    department_head = DepartmentHead.query.get(dept_head_id)
    if not department_head:
        return jsonify({"error": "Department head not found"}), 404

    db.session.delete(department_head)
    db.session.commit()

    return jsonify({"message": "Department head deleted successfully"}), 200

# Get Departments
@departmentInfo.route("/departments", methods=["GET"])
def get_departments():
    depts = Department.query.all()
    departments = [{"id": dept.id, "name": dept.name, "code": dept.code} for dept in depts]
    return jsonify({"departments": departments})

# Create Department
@departmentInfo.route('/departments/register', methods=['POST'])
def create_department():
    data = request.get_json()

    dept = Department(
        name=data["name"],
        code=data["code"]
    )

    db.session.add(dept)
    db.session.commit()

    return jsonify({"message": "Successfully added department"}), 201

# Update Department
@departmentInfo.route('/departments/<int:dept_id>', methods=['PUT'])
def update_department(dept_id):
    department = Department.query.get(dept_id)
    if not department:
        return jsonify({"error": "Department not found"}), 404

    data = request.get_json()

    if "name" in data:
        department.name = data["name"]
    if "code" in data:
        if Department.query.filter(Department.code == data["code"], Department.id != dept_id).first():
            return jsonify({"error": "Department code already exists"}), 400
        department.code = data["code"]

    db.session.commit()

    return jsonify(department.to_dict()), 200

# Delete Department
@departmentInfo.route('/departments/<int:dept_id>', methods=['DELETE'])
def delete_department(dept_id):
    department = Department.query.get(dept_id)
    if not department:
        return jsonify({"error": "Department not found"}), 404

    db.session.delete(department)
    db.session.commit()

    return jsonify({"message": "Department deleted successfully"}), 200
