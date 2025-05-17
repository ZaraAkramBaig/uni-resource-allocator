from app import create_app
from flask_cors import CORS
from App.models import db
# from App.schedule import initialize_database


app = create_app()
CORS(app)

with app.app_context():
    db.create_all()  # Create database tables if they don't exist
    # initialize_database()

if __name__ == '__main__':
    app.run(debug=True)
