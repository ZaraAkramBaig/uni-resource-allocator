from flask import Blueprint, request, jsonify
from models.students import Program
from models import db

program_bp = Blueprint('program', __name__)

@program_bp.route('/program', methods=['POST'])
def create_program():
    data = request.json
    program = Program(
        name=data['name'],
        duration_years=data.get('duration_years')  # Optional field
    )
    db.session.add(program)
    db.session.commit()
    return jsonify({'message': 'Program created', 'program': program_to_dict(program)}), 201

@program_bp.route('/program/<int:id>', methods=['PUT'])
def update_program(id):
    program = Program.query.get_or_404(id)
    data = request.json
    program.name = data.get('name', program.name)
    program.duration_years = data.get('duration_years', program.duration_years)
    db.session.commit()
    return jsonify({'message': 'Program updated', 'program': program_to_dict(program)})

@program_bp.route('/program/<int:id>', methods=['DELETE'])
def delete_program(id):
    program = Program.query.get_or_404(id)
    db.session.delete(program)
    db.session.commit()
    return jsonify({'message': 'Program deleted'})

@program_bp.route('/program', methods=['GET'])
def get_all_programs():
    programs = Program.query.all()
    return jsonify([program_to_dict(p) for p in programs])

@program_bp.route('/program/<int:id>', methods=['GET'])
def get_program(id):
    program = Program.query.get_or_404(id)
    return jsonify(program_to_dict(program))

def program_to_dict(program):
    return {
        'id': program.id,
        'name': program.name,
        'duration_years': program.duration_years
    }
