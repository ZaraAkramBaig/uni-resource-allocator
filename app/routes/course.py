# from flask import Blueprint, jsonify, request
# from app.models.course import Course
# from app import db

# bp = Blueprint('courses', __name__)

# @bp.route('/', methods=['GET'])
# def get_courses():
#     courses = Course.query.all()
#     return jsonify([course.to_dict() for course in courses])

# @bp.route('/<int:id>', methods=['GET'])
# def get_course(id):
#     course = Course.query.get_or_404(id)
#     return jsonify(course.to_dict())

# @bp.route('/', methods=['POST'])
# def create_course():
#     data = request.get_json()
    
#     required_fields = ['code', 'name', 'department_id']
#     if not all(field in data for field in required_fields):
#         return jsonify({'error': 'Missing required fields'}), 400
        
#     course = Course(
#         code=data['code'],
#         name=data['name'],
#         department_id=data['department_id'],
#         faculty_id=data.get('faculty_id'),
#         classroom_id=data.get('classroom_id'),
#         schedule_day=data.get('schedule_day'),
#         start_time=data.get('start_time'),
#         end_time=data.get('end_time')
#     )
    
#     # Check for schedule conflicts
#     if course.classroom_id and course.schedule_day:
#         conflicts = Course.query.filter_by(
#             classroom_id=course.classroom_id,
#             schedule_day=course.schedule_day
#         ).filter(
#             (Course.start_time <= course.end_time) & 
#             (Course.end_time >= course.start_time)
#         ).first()
        
#         if conflicts:
#             return jsonify({'error': 'Schedule conflict detected'}), 400
    
#     db.session.add(course)
#     db.session.commit()
    
#     return jsonify(course.to_dict()), 201

from flask import Blueprint, jsonify, request
from app.models.course import Course
from app.schemas import CourseSchema
from app.auth import admin_required, faculty_required
from app import db
import logging
from datetime import datetime

bp = Blueprint('courses', __name__)
logger = logging.getLogger(__name__)
course_schema = CourseSchema()
courses_schema = CourseSchema(many=True)

@bp.route('/', methods=['GET'])
@faculty_required()
def get_courses():
    courses = Course.query.all()
    logger.info(f"Retrieved {len(courses)} courses")
    return jsonify(courses_schema.dump(courses))

@bp.route('/<int:id>', methods=['GET'])
@faculty_required()
def get_course(id):
    course = Course.query.get_or_404(id)
    logger.info(f"Retrieved course {id}")
    return jsonify(course_schema.dump(course))

@bp.route('/', methods=['POST'])
@admin_required()
def create_course():
    data = course_schema.load(request.get_json())
    
    # Check for schedule conflicts
    if data.get('classroom_id') and data.get('schedule_day'):
        conflicts = Course.query.filter_by(
            classroom_id=data['classroom_id'],
            schedule_day=data['schedule_day']
        ).filter(
            (Course.start_time <= data['end_time']) & 
            (Course.end_time >= data['start_time'])
        ).first()
        
        if conflicts:
            logger.warning(f"Schedule conflict detected for classroom {data['classroom_id']}")
            return jsonify({'error': 'Schedule conflict detected'}), 400
    
    course = Course(**data)
    db.session.add(course)
    db.session.commit()
    
    logger.info(f"Created new course: {course.name}")
    return jsonify(course_schema.dump(course)), 201

@bp.route('/<int:id>', methods=['PUT'])
@admin_required()
def update_course(id):
    course = Course.query.get_or_404(id)
    data = course_schema.load(request.get_json(), partial=True)
    
    # Check for schedule conflicts if updating schedule
    if ('classroom_id' in data or 'schedule_day' in data or 
        'start_time' in data or 'end_time' in data):
        
        classroom_id = data.get('classroom_id', course.classroom_id)
        schedule_day = data.get('schedule_day', course.schedule_day)
        start_time = data.get('start_time', course.start_time)
        end_time = data.get('end_time', course.end_time)
        
        conflicts = Course.query.filter(
            Course.id != id,
            Course.classroom_id == classroom_id,
            Course.schedule_day == schedule_day,
            Course.start_time <= end_time,
            Course.end_time >= start_time
        ).first()
        
        if conflicts:
            logger.warning(f"Schedule conflict detected for course {id}")
            return jsonify({'error': 'Schedule conflict detected'}), 400
    
    for key, value in data.items():
        setattr(course, key, value)
    
    db.session.commit()
    logger.info(f"Updated course {id}")
    return jsonify(course_schema.dump(course))

@bp.route('/<int:id>', methods=['DELETE'])
@admin_required()
def delete_course(id):
    course = Course.query.get_or_404(id)
    db.session.delete(course)
    db.session.commit()
    logger.info(f"Deleted course {id}")
    return '', 204