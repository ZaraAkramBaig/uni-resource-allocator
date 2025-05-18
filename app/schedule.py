from App.models.time import Time
from flask import Blueprint, request, jsonify
from App.models.section import Section
from App.models.schedule import Schedule
from App.models.year import Year
from App.models.timeSlot import TimeSlot
from App.models import db

schedule = Blueprint("schedule",__name__)




def schedule_to_dict(department_id, institution_id, teacher):
    """Convert database schedule into nested dict using index lookups (O(n²)), ensures all 4 years are included."""

    # Step 1: Bulk fetch everything
    years = Year.query.all()
    sections = Section.query.all()
    schedules = Schedule.query.all()
    if teacher: time_slots = TimeSlot.query.filter_by(department_id=department_id, institution_id=institution_id, teacher=teacher).all()
    else: time_slots = TimeSlot.query.filter_by(department_id=department_id, institution_id=institution_id).all()
    

    # Step 2: Create ID-to-object maps for quick lookup
    year_map = {year.id: year.name for year in years}
    section_map = {section.id: (section.name, section.year_id) for section in sections}
    schedule_map = {schedule.id: (schedule.day, schedule.section_id) for schedule in schedules}
    # Step 3: Initialize empty structure for all years and sections
    result = {}
    for section in sections:
        section_name, year_id = section.name, section.year_id
        year_name = year_map.get(year_id)
        if year_name not in result:
            result[year_name] = {}
        if section_name not in result[year_name]:
            result[year_name][section_name] = {}
    # Step 4: Fill structure using time slots
    for slot in time_slots:
        schedule_id = slot.schedule_id
        if schedule_id not in schedule_map:
            continue

        day, section_id = schedule_map[schedule_id]
        if section_id not in section_map:
            continue

        section_name, year_id = section_map[section_id]
        year_name = year_map.get(year_id)

        # Ensure day dictionary exists
        if day not in result[year_name][section_name]:
            result[year_name][section_name][day] = {}

        # Add slot
        result[year_name][section_name][day][slot.time] = {
            "subject": slot.subject,
            "teacher": slot.teacher,
            "room": slot.room,
            "type": slot.type,
            "department_id": slot.department_id,
            "institution_id": slot.institution_id,
            "time_ID": slot.time_ID
        }

    return result

def scheduleByYear(department_id, institution_id, year_name, section_name):
    """Get schedule for specific year and section."""
    
    # Step 1: Get the year and section objects
    year = Year.query.filter_by(name=year_name).first()
    if not year:
        return {"error": "Year not found"}
        
    section = Section.query.filter_by(year_id=year.id, name=section_name).first()
    if not section:
        return {"error": "Section not found"}
    
    # Step 2: Get all schedules for this section
    schedules = Schedule.query.filter_by(section_id=section.id).all()
    schedule_ids = [schedule.id for schedule in schedules]
    
    # Step 3: Get all time slots for these schedules with matching department and institution
    time_slots = TimeSlot.query.filter(
        TimeSlot.schedule_id.in_(schedule_ids),
        TimeSlot.department_id == department_id,
        TimeSlot.institution_id == institution_id
    ).all()
    
    # Step 4: Create a mapping of schedule_id to day for faster lookup
    schedule_day_map = {schedule.id: schedule.day for schedule in schedules}
    
    # Step 5: Initialize result structure
    result = {
        year_name: {
            section_name: {}
        }
    }
    
    # Step 6: Fill the structure with time slots
    for slot in time_slots:
        day = schedule_day_map[slot.schedule_id]
        
        # Ensure day dictionary exists
        if day not in result[year_name][section_name]:
            result[year_name][section_name][day] = {}
        
        # Add slot
        result[year_name][section_name][day][slot.time] = {
            "subject": slot.subject,
            "teacher": slot.teacher,
            "room": slot.room,
            "type": slot.type,
            "department_id": slot.department_id,
            "institution_id": slot.institution_id,
            "time_ID": slot.time_ID
        }
    
    return result


# API Routes
@schedule.route('/schedule/<institution_id>/<department_id>', methods=['GET'])
def get_schedule(institution_id, department_id):
    """Get the entire schedule."""
    return jsonify(schedule_to_dict(institution_id, department_id, None))

@schedule.route('/schedule/<institution_id>/<department_id>/<teacher>', methods=['GET'])
def get_schedule_for_teacher(institution_id, department_id, teacher):
    """Get the entire schedule."""
    return jsonify(schedule_to_dict(institution_id, department_id, teacher))


@schedule.route('/schedule/<institution_id>/<department_id>/<year>/<section>', methods=['GET'])
def get_schedule_by_year_section(institution_id, department_id, year, section):
    """Get the entire schedule."""
    return jsonify(scheduleByYear(institution_id, department_id,year, section))



@schedule.route('/schedule/<year_name>/<section_name>', methods=['POST'])
def create_schedule(year_name, section_name):
    """Create schedule for a specific year, section."""
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    # Find or create the required database objects
    year = Year.query.filter_by(name=year_name).first()
    if not year:
        year = Year(name=year_name)
        db.session.add(year)
        db.session.commit()
    
    section = Section.query.filter_by(name=section_name, year_id=year.id).first()
    if not section:
        section = Section(name=section_name, year_id=year.id)
        db.session.add(section)
        db.session.commit()
    
    schedule_obj = Schedule.query.filter_by(section_id=section.id).all()

    for day in schedule_obj:
        day_name = day.day  # Assuming Schedule table has a 'day' column like 'Monday'
        
        # Skip if no data for this day
        if day_name not in data:
            continue
        TimeSlot.query.filter_by(schedule_id=day.id).delete()
        
        day_data = data[day_name]  # e.g., {'8:00 AM': {...}, '9:00 AM': {...}}

        new_slots = []
        new_slots_json = []
        
        for time_str, slot_data in day_data.items():
            print(time_str, slot_data)
            if not slot_data:
                continue
            new_slot = TimeSlot(
                time=time_str,
                subject=slot_data.get('subject', ''),
                teacher=slot_data.get('teacher', ''),
                room=slot_data.get('room', ''),
                type=slot_data.get('type', ''),
                schedule_id=day.id,
                institution_id=slot_data.get('institution_id'),
                department_id=slot_data.get('department_id'),
                time_ID=slot_data.get("time_ID"),
                teacher_id=slot_data.get("teacher_id")
            )
            new_slots.append(new_slot)
            new_slots_json.append({time_str: {
                "subject": new_slot.subject,
                "teacher": new_slot.teacher,
                "room": new_slot.room,
                "type": new_slot.type,
                "department_id": new_slot.department_id,
                "institution_id": new_slot.institution_id,
                "time_ID": new_slot.time_ID
            }})
        
        if new_slots:
            db.session.add_all(new_slots)
    db.session.commit()
    return jsonify({"message": "Schedule created successfully", "time": new_slots_json}), 201


@schedule.route('/time/<institution_id>/<department_id>', methods=['POST'])
def create_time(institution_id, department_id):
    data = request.get_json()
    if len(data) > 0:
        tList = []
        for time in data:
            t = Time.query.filter_by(department_id=department_id, institution_id=institution_id,time=time).first()
            if t is not None:
                continue
            else:
                new_time = Time(
                    time=time,
                    department_id=department_id,  # Corrected parameter assignment
                    institution_id=institution_id  # Corrected parameter assignment
                )
                db.session.add(new_time)
                db.session.commit()
                
                # Fixed dictionary structure - removed the extra nested braces
                tList.append({
                    'id': new_time.id,
                    'time': new_time.time,
                    'department_id': new_time.department_id,
                    'institution_id': new_time.institution_id
                })
                
    return jsonify({"message": "Time created successfully", "time": tList}), 200
        
    

@schedule.route('/time/<institution_id>/<department_id>', methods=['GET'])
def get_all_times(institution_id, department_id):
    """Get all time slots with optional filters"""
    try:
        query = Time.query
        
        if department_id:
            query = query.filter_by(department_id=department_id)
        
        if institution_id:
            query = query.filter_by(institution_id=institution_id)
        
        times = query.all()
        
        # Format response
        time_list = [
            {
                'id': time.id,
                'time': time.time,
                'department_id': time.department_id,
                'institution_id': time.institution_id
            }
            for time in times
        ]
        
        return jsonify({'times': time_list}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@schedule.route('/time/<int:time_id>', methods=['DELETE'])
def delete_time(time_id):
    """Delete a specific time slot by ID"""
    try:
        time = Time.query.get(time_id)
        
        if not time:
            return jsonify({'error': 'Time slot not found'}), 404
        
        db.session.delete(time)
        db.session.commit()
        
        return jsonify({'message': f'Time slot with ID {time_id} deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
@schedule.route('/timeSlot/<int:time_id>', methods=['DELETE'])
def delete_timeSlot(time_id):
    """Delete a specific time slot by ID"""
    time = TimeSlot.query.filter_by(time_ID=time_id).all()
    
    for t in time:
        db.session.delete(t)
        db.session.commit()
    
    return jsonify({'message': f'Time slot with ID {time_id} deleted successfully'}), 200
        