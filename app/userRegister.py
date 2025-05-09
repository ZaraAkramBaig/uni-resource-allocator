from flask import Blueprint, jsonify, request
from .models import db
from .models.user import User
import bcrypt

userInfo = Blueprint("user", __name__)

@userInfo.route("/user/register", methods=["POST"])
def register_user():
    data = request.get_json()
    print(data)
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

@userInfo.route("/user/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()

    # Check if the user exists
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    if data.email in data:
        user.email = data.get("email", user.email)
    if data.password in data:
        user.password= bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt(10)).decode('utf-8'),
    return jsonify({"message": "User updated successfully"}), 200


