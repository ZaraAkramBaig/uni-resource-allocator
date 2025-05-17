from App.models import db
class Year(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)  # "1st Year", "2nd Year", etc.
    sections = db.relationship('Section', backref='year', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Year {self.name}>'