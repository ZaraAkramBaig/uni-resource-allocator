from flask import Blueprint, jsonify, request
from App.models import db
from App.models.user import User
import bcrypt

userInfo = Blueprint("user", __name__)

@userInfo.route("/user/register", methods=["POST"])
def register_user():
    data = request.get_json()
    # Check if the user already exists
    existing_user = User.query.filter_by(email=data["email"]).first()
    if existing_user:
        return jsonify({"message": "User already exists"}), 409

    # Create new user instance
    new_user = User(
        email=data["email"],
        password= bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt(10)).decode('utf-8'),
        role=data["role"],
        institution_id=data["institution_id"],
        department_id=data["department_id"]
    )

    # Add to database
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
    "message": "User registered successfully", 
    "user": {
        "id": new_user.id,
        "email": new_user.email,
        "role": new_user.role
    }
}), 201

@userInfo.route('/user/<int:id>', methods=['DELETE'])
def delete_teacher(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'})

@userInfo.route('/user/dept/<int:id>', methods=['DELETE'])
def delete_users_by_department(id):
    users = User.query.filter_by(department_id=id).all()
    for user in users:
        db.session.delete(user)
    db.session.commit()
    return jsonify({'message': f'{len(users)} user(s) deleted from department {id}'})


@userInfo.route('/user/institution/<string:id>', methods=['DELETE'])
def delete_users_by_institution(id):
    users = User.query.filter_by(institution_id=id).all()
    for user in users:
        db.session.delete(user)
    db.session.commit()
    return jsonify({'message': f'{len(users)} user(s) deleted from institution {id}'})
