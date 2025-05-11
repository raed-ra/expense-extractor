from flask import Blueprint, render_template, g, request, flash, redirect, url_for
from flask_login import login_required
from db import get_db
from models import Transaction
from datetime import datetime

# create a blueprint for the record route
record_bp = Blueprint('record', __name__, url_prefix='/record')

@record_bp.route('/', methods=('GET', 'POST'))
@login_required
def index():
    db = get_db()
    
    # handle form submission
    if request.method == 'POST':
        amount = request.form.get('amount')
        category = request.form.get('category')
        date = request.form.get('date')
        description = request.form.get('description')
        transaction_type = request.form.get('type', 'expense')
        
        error = None
        
        if not amount:
            error = 'Amount cannot be empty'
        elif not category:
            error = 'Category cannot be empty'
        elif not date:
            error = 'Date cannot be empty'
            
        if error is None:
            try:
                # create a new transaction record
                transaction = Transaction(
                    amount=float(amount),
                    type=transaction_type,
                    category=category,
                    date=datetime.strptime(date, '%Y-%m-%d').date(),
                    user_id=g.user.id,
                    description=description,
                    created_at=datetime.now()
                )
                
                db.add(transaction)
                db.commit()
                flash('Record created successfully', 'success')
                return redirect(url_for('record.index'))
                
            except Exception as e:
                db.rollback()
                error = f'Failed to create record: {str(e)}'
        
        flash(error, 'error')
    
    return render_template(
        'main/record.html', 
        active_page='record'
    )
