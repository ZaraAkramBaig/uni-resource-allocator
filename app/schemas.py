# from marshmallow import Schema, fields, validate

# class DepartmentSchema(Schema):
#     id = fields.Int(dump_only=True)
#     name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
#     code = fields.Str(required=True, validate=validate.Length(min=1, max=10))

# class FacultySchema(Schema):
#     id = fields.Int(dump_only=True)
#     name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
#     email = fields.Email(required=True)
#     department_id = fields.Int(required=True)

# class StudentSchema(Schema):
#     id = fields.Int(dump_only=True)
#     name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
#     email = fields.Email(required=True)
#     student_id = fields.Str(required=True, validate=validate.Length(min=1, max=20))

# class ClassroomSchema(Schema):
#     id = fields.Int(dump_only=True)
#     room_number = fields.Str(required=True, validate=validate.Length(min=1, max=20))
#     capacity = fields.Int(required=True, validate=validate.Range(min=1))
#     is_lab = fields.Bool()

# class CourseSchema(Schema):
#     id = fields.Int(dump_only=True)
#     code = fields.Str(required=True, validate=validate.Length(min=1, max=20))
#     name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
#     department_id = fields.Int(required=True)
#     faculty_id = fields.Int()
#     classroom_id = fields.Int()
#     schedule_day = fields.Str(validate=validate.OneOf(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']))
#     start_time = fields.Time()
#     end_time = fields.Time()

# class UserSchema(Schema):
#     id = fields.Int(dump_only=True)
#     username = fields.Str(required=True, validate=validate.Length(min=3, max=80))
#     email = fields.Email(required=True)
#     password = fields.Str(required=True, load_only=True, validate=validate.Length(min=6))
#     role = fields.Str(required=True, validate=validate.OneOf(['admin', 'faculty', 'student']))

from marshmallow import Schema, fields, validate, validates, ValidationError
from app.models.user import User

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True)
    username = fields.Str(required=True, validate=validate.Length(min=3, max=80))
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=6))
    first_name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    last_name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    role = fields.Str(required=True, validate=validate.OneOf(['super_admin', 'admin', 'faculty', 'student']))
    university_id = fields.Int()
    department_id = fields.Int()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @validates('email')
    def validate_email(self, value):
        if User.query.filter_by(email=value).first():
            raise ValidationError('Email already exists')

    @validates('username')
    def validate_username(self, value):
        if User.query.filter_by(username=value).first():
            raise ValidationError('Username already exists')

class UniversitySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    code = fields.Str(required=True, validate=validate.Length(min=1, max=20))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class NotificationSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    content = fields.Str(required=True)
    sender_id = fields.Int(required=True)
    department_id = fields.Int()
    course_id = fields.Int()
    created_at = fields.DateTime(dump_only=True)