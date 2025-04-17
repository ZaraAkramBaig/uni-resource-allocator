# from flask import Blueprint, jsonify, request
# from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
# from app.models.user import User
# from app import db

# bp = Blueprint('auth', __name__)

# @bp.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
    
#     if not data or not data.get('username') or not data.get('password'):
#         return jsonify({'error': 'Missing username or password'}), 400
        
#     user = User.query.filter_by(username=data['username']).first()
#     if not user or not user.check_password(data['password']):
#         return jsonify({'error': 'Invalid username or password'}), 401
    
#     access_token = create_access_token(
#         identity=user.id,
#         additional_claims={'role': user.role}
#     )
    
#     return jsonify({
#         'access_token': access_token,
#         'user': user.to_dict()
#     })

# @bp.route('/register', methods=['POST'])
# def register():
#     data = request.get_json()
    
#     required_fields = ['username', 'email', 'password', 'role']
#     if not all(field in data for field in required_fields):
#         return jsonify({'error': 'Missing required fields'}), 400
    
#     if User.query.filter_by(username=data['username']).first():
#         return jsonify({'error': 'Username already exists'}), 400
        
#     if User.query.filter_by(email=data['email']).first():
#         return jsonify({'error': 'Email already exists'}), 400
    
#     user = User(
#         username=data['username'],
#         email=data['email'],
#         role=data['role']
#     )
#     user.set_password(data['password'])
    
#     db.session.add(user)
#     db.session.commit()
    
#     return jsonify(user.to_dict()), 201

# @bp.route('/me', methods=['GET'])
# @jwt_required()
# def get_current_user():
#     user_id = get_jwt_identity()
#     user = User.query.get_or_404(user_id)
#     return jsonify(user.to_dict())

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from app.models.user import User
from app.models.university import University
from app import db
from app.schemas import UserSchema
import logging

bp = Blueprint('auth', __name__)
logger = logging.getLogger(__name__)
user_schema = UserSchema()

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['email', 'username', 'password', 'first_name', 'last_name', 'role']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Validate role
    valid_roles = ['super_admin', 'admin', 'faculty', 'student']
    if data['role'] not in valid_roles:
        return jsonify({'error': 'Invalid role'}), 400
    
    # Check if user already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already taken'}), 400
    
    # For roles other than super_admin, validate university_id
    if data['role'] != 'super_admin':
        if 'university_id' not in data:
            return jsonify({'error': 'University ID required for this role'}), 400
        university = University.query.get(data['university_id'])
        if not university:
            return jsonify({'error': 'Invalid university ID'}), 400
    
    # Create new user
    user = User(
        email=data['email'],
        username=data['username'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        role=data['role'],
        university_id=data.get('university_id'),
        department_id=data.get('department_id')
    )
    user.set_password(data['password'])
    
    try:
        db.session.add(user)
        db.session.commit()
        logger.info(f"Created new user: {user.username}")
        return jsonify(user.to_dict()), 201
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Error creating user'}), 500

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Missing username or password'}), 400
        
    user = User.query.filter_by(username=data['username']).first()
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid username or password'}), 401
    
    access_token = create_access_token(
        identity=user.id,
        additional_claims={
            'role': user.role,
            'university_id': user.university_id,
            'department_id': user.department_id
        }
    )
    
    return jsonify({
        'access_token': access_token,
        'user': user.to_dict()
    })

@bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())