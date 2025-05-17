from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token
from App.models.user import User
import bcrypt

auth = Blueprint("auth",__name__)


@auth.route('/login', methods=['POST'])
def login():
    email = request.json.get("email")
    password = request.json.get("password")

    user_from_db = User.query.filter_by(email=email).first()
    
    if not user_from_db:
        return jsonify(message="User does not Exist"), 401
    if not bcrypt.checkpw(password.encode('utf-8'), user_from_db.password.encode('utf-8')):
        print("hello")
        return jsonify(message="Incorrect Password"), 401

    access_token = create_access_token(identity={
        "id" : user_from_db.id,
        "email": user_from_db.email,
        "role" : user_from_db.role,
        "institution_id":  user_from_db.institution_id,
        "department_id":  user_from_db.department_id,
        })
    # refresh_token = create_refresh_token(identity=user_from_db)
    return jsonify(access_token=access_token)

