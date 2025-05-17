from App.models import db

class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)  # "Section A", "Section B", etc.
    year_id = db.Column(db.Integer, db.ForeignKey('year.id'), nullable=False)
    schedules = db.relationship('Schedule', backref='section', cascade='all, delete-orphan')

    __table_args__ = (db.UniqueConstraint('name', 'year_id', name='_section_year_uc'),)

    def __repr__(self):
        return f'<Section {self.name} of {self.year.name}>'