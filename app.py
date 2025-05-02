from flask import Flask, render_template

def create_app():
   
    # Initialize the Flask application
    app = Flask(__name__)
    
    # Configure the application
    app.config['SECRET_KEY'] = 'your-secret-key'  # Change this in production
    
    # Register routes
    
    # Define the route for the homepage
    @app.route('/')
    def index():
        return 'Welcome to ExpenseManager! Go to <a href="/login">login page</a> or <a href="/register">register page</a>'
    
    # Define the route for the login page
    @app.route('/login')
    def login():
        return render_template('auth/login.html')
    
    # Define the route for the registration page
    @app.route('/register')
    def register():
        return render_template('auth/register.html')
    
    return app

# Create the application using the factory function
app = create_app()

if __name__ == '__main__':
    # Enable debug mode for development
    app.run(debug=True)
