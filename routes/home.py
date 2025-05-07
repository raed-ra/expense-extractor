from flask import Blueprint, render_template, g
from flask_login import login_required  # if you're using Flask-Login

home_bp = Blueprint('home', __name__, url_prefix='/home')

@home_bp.route('/')
@login_required  # Optional: use only if auth is in place
def home():
    return render_template('main/index.html')