# from functools import wraps
# from flask import jsonify
# from flask_jwt_extended import get_jwt, verify_jwt_in_request

# def role_required(allowed_roles):
#     def decorator(fn):
#         @wraps(fn)
#         def wrapper(*args, **kwargs):
#             verify_jwt_in_request()
#             claims = get_jwt()
#             if claims.get('role') not in allowed_roles:
#                 return jsonify({'error': 'Insufficient permissions'}), 403
#             return fn(*args, **kwargs)
#         return wrapper
#     return decorator

# # Convenience decorators for common roles
# def admin_required():
#     return role_required(['admin'])

# def faculty_required():
#     return role_required(['admin', 'faculty'])

# def student_required():
#     return role_required(['admin', 'faculty', 'student'])

from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt, verify_jwt_in_request

def role_required(allowed_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get('role') not in allowed_roles:
                return jsonify({'error': 'Insufficient permissions'}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator

# Role-specific decorators
def super_admin_required():
    return role_required(['super_admin'])

def admin_required():
    return role_required(['super_admin', 'admin'])

def faculty_required():
    return role_required(['super_admin', 'admin', 'faculty'])

def student_required():
    return role_required(['super_admin', 'admin', 'faculty', 'student'])

# University-specific authorization
def same_university_required():
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if 'university_id' not in kwargs or claims.get('university_id') != kwargs['university_id']:
                return jsonify({'error': 'Access restricted to own university'}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator

# Department-specific authorization
def same_department_required():
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if 'department_id' not in kwargs or claims.get('department_id') != kwargs['department_id']:
                return jsonify({'error': 'Access restricted to own department'}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator