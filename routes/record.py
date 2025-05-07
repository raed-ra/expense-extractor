# routes/record.py
from flask import Blueprint, render_template, g
from flask_login import login_required  # if you're using Flask-Login

record_bp = Blueprint('record', __name__, url_prefix='/record')


@record_bp.route('/index')
@login_required  # Optional: use only if auth is in place
def index():
    return render_template('main/index.html')

