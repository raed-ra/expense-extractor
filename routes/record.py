from flask import Blueprint, render_template, g, request, flash, redirect, url_for, session, jsonify
from flask_login import login_required, current_user
from db import get_db
from models.transaction import Transaction
from datetime import datetime
from sqlalchemy import and_
import math

record_bp = Blueprint('record', __name__, url_prefix='/record')

@record_bp.route('/', methods=('GET', 'POST'))
@login_required
def index():
    db = get_db()
    if request.method == 'POST':
        try:
            amount = request.form.get('amount')
            category = request.form.get('category')
            date = request.form.get('date')
            description = request.form.get('description')
            user_id = session.get('user_id')
            record_type = request.form.get('record_type')

            error = None
            if not amount:
                error = 'Amount cannot be empty'
            elif not category:
                error = 'Category cannot be empty'
            elif not date:
                error = 'Date cannot be empty'

            if error is None:
                try:
                    record = Transaction(
                        user_id=g.user.id,
                        category=category,
                        type=record_type,
                        amount=float(amount),
                        date=datetime.strptime(date, '%Y-%m-%d').date(),
                        description=description,
                    )
                    db.add(record)
                    db.commit()
                    flash('Record created successfully', 'success')
                    return redirect(url_for('record.index'))
                except Exception as e:
                    db.rollback()
                    error = f'Failed to create record: {str(e)}'
            if error:
                flash(error, 'error')
        except Exception as e:
            flash('An unexpected error occurred', 'error')
    return render_template('main/record.html', active_page='record')


