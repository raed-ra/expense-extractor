# /routes/auth/login.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import SessionLocal
from models import User
from sqlalchemy.exc import SQLAlchemyError

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        db = SessionLocal()
        try:
            user = db.query(User).filter_by(email=email).first()
            if user and user.password == password:  # Replace with hashed password check later
                flash('Logged in successfully!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Invalid email or password.', 'error')
        except SQLAlchemyError as e:
            flash('Database error during login.', 'error')
            print(e)
        finally:
            db.close()

    return render_template('auth/login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm = request.form.get('confirm_password')

        if password != confirm:
            flash('Passwords do not match.', 'error')
            return render_template('auth/register.html')

        db = SessionLocal()
        try:
            # Check if email already exists
            existing = db.query(User).filter_by(email=email).first()
            if existing:
                flash('Email already registered.', 'error')
                return render_template('auth/register.html')

            # Create user and save
            new_user = User(email=email, username=username, password=password)
            db.add(new_user)
            db.commit()

            flash('Registered successfully! Please log in.', 'success')
            return redirect(url_for('auth.login'))

        except SQLAlchemyError as e:
            db.rollback()
            flash('Error during registration.', 'error')
            print(e)
        finally:
            db.close()

    return render_template('auth/register.html')
