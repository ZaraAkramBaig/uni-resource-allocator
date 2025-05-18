from flask import Blueprint, jsonify, request
from App.models import db
from App.models.department import Department
from App.models.department_head import DepartmentHead

departmentInfo = Blueprint("department", __name__)

# --------------------- Department Head Routes ---------------------

# Create Department Head
@departmentInfo.route('/department_heads/register', methods=['POST'])
def create_department_head():
    data = request.get_json()

    if not all(k in data for k in ("name", "email", "department_id", "institution_id")):
        return jsonify({"error": "Missing required fields"}), 400
    if DepartmentHead.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already exists"}), 400
    if DepartmentHead.query.filter_by(department_id=data["department_id"]).first():
        return jsonify({"error": "Head already exists"}), 400

    new_department_head = DepartmentHead(
        name=data["name"],
        email=data["email"],
        department_id=data["department_id"],
        institution_id=data["institution_id"],
        user_id=data["user_id"],
    )
    db.session.add(new_department_head)
    db.session.commit()

    return jsonify({"message": "Department head created successfully", "new_department_head": {
        "id": new_department_head.id,
            "name": new_department_head.name,
            "email": new_department_head.email,
            "department_id": new_department_head.department_id,
            "institution_id": new_department_head.institution_id,
            "user_id": new_department_head.user_id
    }}), 201


# Get All Department Heads with specific institution
@departmentInfo.route('/department_heads/<string:inst_id>', methods=['GET'])
def get_department_heads(inst_id):
    heads = DepartmentHead.query.filter_by(institution_id=inst_id).all()
    deptHeads = []
    for head in heads:
        dept_dict = {
            "id": head.id,
            "name": head.name,
            "email": head.email,
            "department_id": head.department_id,
            "institution_id": head.institution_id,
            "user_id": head.user_id
        }
        deptHeads.append(dept_dict)
    return jsonify({
        "department_heads": deptHeads,
        "message": f"Found {len(heads)} department head(s)"
    }), 200



# Delete Department Head
@departmentInfo.route('/department_heads/<string:dept_head_id>', methods=['DELETE'])
def delete_department_head(dept_head_id):
    department_head = DepartmentHead.query.get(dept_head_id)
    if not department_head:
        return jsonify({"error": "Department head not found"}), 404

    db.session.delete(department_head)
    db.session.commit()

    return jsonify({"message": "Department head deleted successfully"}), 200


# --------------------- Department Routes ---------------------

# Get Departments
@departmentInfo.route("/departments/<string:inst_id>", methods=["GET"])
def get_departments(inst_id):
    depts = Department.query.filter_by(institution_id=inst_id).all()
    departments = []
    for dept in depts:
        dept_dict = {
            "id": dept.id,
            "name": dept.name,
            "code": dept.code,
        }
        departments.append(dept_dict)

    return jsonify({"departments": departments, "message": f"Found {len(departments)} department(s)"}), 200

#Get department by id
@departmentInfo.route("/department/<id>", methods=["GET"])
def get_department_by_id(id):
    dept = Department.query.filter_by(id=id).first()
    dept_dict = {
        "id": dept.id,
        "name": dept.name,
        "code": dept.code,
    }

    return jsonify({"department": dept_dict}), 200


# Create Department
@departmentInfo.route('/departments/register', methods=['POST'])
def create_department():
    data = request.get_json()

    dept = Department(
        name=data["name"],
        code=data["code"],
        institution_id=data["institution_id"]
    )

    db.session.add(dept)
    db.session.commit()

    return jsonify({"message": "Department created successfully", "dept": {
        "id": dept.id,
        "name": dept.name,
        "code": dept.code,
    }}), 201


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

    return jsonify({"message": "Department updated successfully", "department": department.to_dict()}), 200


# Delete Department
@departmentInfo.route('/departments/<int:dept_id>', methods=['DELETE'])
def delete_department(dept_id):
    department = Department.query.get(dept_id)
    if not department:
        return jsonify({"error": "Department not found"}), 404

    db.session.delete(department)
    db.session.commit()

    return jsonify({"message": "Department deleted successfully"}), 200
