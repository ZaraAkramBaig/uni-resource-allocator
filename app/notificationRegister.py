from flask import Blueprint, request, jsonify
from App.models.notification import Notification
from App.models import db
from datetime import datetime
from sqlalchemy import or_

notification = Blueprint("notification", __name__)

def update(id, teacher):
    data = request.json
    notify = Notification.query.filter_by(id=id).first()
        
    if not notify:
        return jsonify({'error': 'Schedule not found'}), 404
    if teacher: 
        notify.acknowledgement = True
    else: 
        notify.status = data["status"] 
        notify.response = data["response"]

    db.session.add(notify)
    db.session.commit()
    return notify

# POST endpoint to store schedule data
@notification.route('/notification/register/<inst_id>/<dept_id>', methods=['POST'])
def create_Notification(inst_id, dept_id):
    data = request.json
    # Parse timestamp if provided, otherwise use current time
    timestamp = data.get('timestamp')
    if timestamp:
        try:
            timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        except ValueError:
            timestamp = datetime.utcnow()
    else:
        timestamp = datetime.utcnow()
    
    new_notification = Notification(
        currentDay=data['currentDay'],
        currentTime=data['currentTime'],
        message=data.get('message', ''),
        preferredDay=data.get('preferredDay'),
        preferredTime=data.get('preferredTime'),
        requestType=data['requestType'],
        status=data.get('status', 'pending'),
        subject=data['subject'],
        teacherId=data['teacherId'],
        teacherName=data['teacherName'],
        timestamp=timestamp,
        response=data.get("response"),
        institution_id=inst_id,
        department_id=dept_id,
        acknowledgement= data.get("acknowledgement")
    )
    
    db.session.add(new_notification)
    db.session.commit()
    
    return jsonify({
        'message': 'Schedule created successfully',
        'notification': new_notification.to_dict()
    }), 201
        

# PUT endpoint to update schedule status
@notification.route('/notification/update/deptHead/<id>', methods=['PUT'])
def update_Notification_for_deptHead(id):
    response = update(id, False)
    return jsonify({
        'message': 'Notification updated successfully',
        'notification': response.to_dict()
    }), 200

@notification.route('/notification/update/<id>', methods=['PUT'])
def update_Notification_for_teacher(id):
    response = update(id, True)
    return jsonify({
        'message': 'Notification updated successfully',
        'notification': response.to_dict()
    }), 200

@notification.route('/notification/<inst_id>/<dept_id>/<teacher_id>', methods=['GET'])
def get_Notification_for_teacher(inst_id, dept_id, teacher_id):
    schedule = Notification.query.filter(
        Notification.institution_id == inst_id,
        Notification.department_id == dept_id,
        Notification.teacherId == teacher_id,
        or_(Notification.status == "Approved", Notification.status == "Rejected")
    ).all()
    
    notifications = []
    
    for n in schedule:
        dic = {
            "id": n.id,
            "currentDay": n.currentDay,
            "currentTime": n.currentTime,
            "message": n.message,
            "preferredDay": n.preferredDay,
            "preferredTime": n.preferredTime,
            "requestType": n.requestType,
            "status": n.status,
            "subject": n.subject,
            "teacherId": n.teacherId,
            "teacherName": n.teacherName,
            "timestamp": n.timestamp.isoformat(),
            "response": n.response,
            "acknowledgement": n.acknowledgement
        }
        notifications.append(dic)
    
    return jsonify({'notifications': notifications})
        

# GET endpoint for department head to view pending requests
@notification.route('/notification/pending/<inst_id>/<dept_id>', methods=['GET'])
def get_pending_schedules(inst_id, dept_id):
    pending_schedules = Notification.query.filter_by(department_id=inst_id, institution_id=dept_id, status='pending').all()
    result = [schedule.to_dict() for schedule in pending_schedules]
    
    return jsonify({'pending_schedules': result})