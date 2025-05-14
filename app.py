# /app.py
from flask import Flask, redirect, url_for
from flask_login import LoginManager, current_user
from dotenv import load_dotenv
from routes import register_routes
import os
from db import Base, engine, init_app, get_db
from models import User, Transaction, Upload, SharedReport, SharedView
from flask import g, request
from flask import render_template

load_dotenv()

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key')

    # Setup login manager
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Register routes
    register_routes(app)


    # Setup DB teardown and CLI
    init_app(app)

    # Set g.user for templates
    @app.before_request
    def load_logged_in_user():
        g.user = current_user if current_user.is_authenticated else None
    
    # Add no cache response header to prevent cached pages from being accessed by logged out users
    @app.after_request
    def add_no_cache_headers(response):
        # Only disable cache for pages that require authentication
        if current_user.is_authenticated or request.endpoint and 'login' not in request.endpoint:
            response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
        return response

    # Sample home route
    @app.route('/')
    def index():
        #return 'Welcome! Go to <a href="/auth/login">Login</a> or <a href="/auth/register">Register</a>'
        return redirect(url_for('auth.login'))
    
    # Register error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        
        return render_template('errors/500.html'), 500
    
    return app

@login_manager.user_loader
def load_user(user_id):
    db = get_db()
    return db.query(User).get(int(user_id))

# Create DB and tables if not already there
if not os.path.exists("expensemanager.db"):
    print("🔧 Creating database and tables...")
    Base.metadata.create_all(bind=engine)
    
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)