from flask import request, jsonify, Blueprint
from App.models import db
from App.models.timeSlot import TimeSlot
from App.models.day import Day

courseSchedule = Blueprint("schedule", __name__)

@courseSchedule.route('/schedule', methods=['POST'])
def save_schedule():
    data = request.get_json()

    for day_name, slots in data.items():
        day = Day(name=day_name)
        db.session.add(day)
        db.session.flush()  # To get the ID for foreign key

        for time, info in slots.items():
            slot = TimeSlot(
                time=time,
                subject=info['subject'],
                teacher=info['teacher'],
                room=info['room'],
                type=info['type'],
                day_id=day.id
            )
            db.session.add(slot)

    db.session.commit()
    return jsonify({'message': 'Schedule saved successfully'}), 201
