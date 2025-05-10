from flask import Blueprint, request, jsonify
from datetime import datetime
from models.course import Course, CourseSchedule
from models import db

course_bp = Blueprint('course', __name__)

@course_bp.route('/courses', methods=['POST'])
def create_course():
    data = request.get_json()

    course = Course(
        code=data['code'],
        name=data['name'],
        department_id=data['department_id'],
        faculty_id=data.get('faculty_id'),
        classroom_id=data.get('classroom_id')
    )
    db.session.add(course)
    db.session.commit()

    schedules = data.get('schedules', [])
    for sched in schedules:
        schedule = CourseSchedule(
            course_id=course.id,
            classroom_id=sched.get('classroom_id', course.classroom_id),
            schedule_day=sched['day'],
            start_time=datetime.strptime(sched['start_time'], "%H:%M").time(),
            end_time=datetime.strptime(sched['end_time'], "%H:%M").time()
        )
        db.session.add(schedule)

    db.session.commit()
    return jsonify({'message': 'Course created with schedule'}), 201
