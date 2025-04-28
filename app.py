# app.py

from flask import Flask
from routes.main import main_bp
from models import db
import os
from dotenv import load_dotenv

# create a Flask application instance
app = Flask(__name__) 
# the key tells Flask where to store uploaded files
app.config['UPLOAD_FOLDER'] = 'uploads' 
# key: tells SQLAlchemy to use SQLite as db and the value is the path to the db file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' 
# key: tells SQLAlchemy to track modifications of objects & emit signals
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# key: tells Flask to use the secret key for session management and CSRF protection
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

load_dotenv()

# Initialize database
db.init_app(app)
with app.app_context():
    db.create_all()

# Register blueprints
app.register_blueprint(main_bp)

if __name__ == '__main__':
    print("✅ App started, initializing DB...")
    app.run(debug=True, port=5000)
