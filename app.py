# /app.py
from flask import Flask
from routes import register_routes
import os
from db import Base, engine
from models import User, Transaction

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
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
