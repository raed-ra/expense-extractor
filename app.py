# /app.py
from flask import Flask
from flask_login import LoginManager
from dotenv import load_dotenv
from routes import register_routes
import os
from db import Base, engine, init_app, get_db
from models import User, Transaction, Upload

load_dotenv() 
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    db = get_db()
    return db.query(User).get(int(user_id))

# Conditionally create DB/tables if not already there
if not os.path.exists("expensemanager.db"):
    print("🔧 Creating database and tables...")
    Base.metadata.create_all(bind=engine)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    
    @app.route('/')
    def index():
        return 'Welcome! Go to <a href="/auth/login">Login</a> or <a href="/auth/register">Register</a>'

    register_routes(app)
    
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Replace with your login endpoint name
    init_app(app)  # only for CLI & teardown setup

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
