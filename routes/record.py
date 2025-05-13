from flask import Blueprint, render_template, g, request, flash, redirect, url_for, session, jsonify
from flask_login import login_required, current_user
from db import get_db
from models.record_list import Record
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
                    record = Record(
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

@record_bp.route('/list', methods=('GET',))
@login_required
def list():
    db = get_db()
    
    # get page number, default is 1
    page = request.args.get('page', 1, type=int)
    
    # number of records per page
    per_page = 5
    
    # get filter parameters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    record_type = request.args.get('type')
    
    # build query conditions
    query_conditions = [Record.user_id == g.user.id]
    
    # add date filter conditions
    if start_date and end_date:
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
        query_conditions.append(Record.date >= start_date_obj)
        query_conditions.append(Record.date <= end_date_obj)
    
    # add transaction type filter conditions
    if record_type in ['income', 'expense']:
        query_conditions.append(Record.type == record_type)
    
    # query total number of records
    total_count = db.query(Record).filter(and_(*query_conditions)).count()
    
    # calculate total number of pages
    total_pages = math.ceil(total_count / per_page) if total_count > 0 else 1
    
    # adjust page number, ensure it is within the valid range
    if page < 1:
        page = 1
    elif page > total_pages:
        page = total_pages
    
    # query records for the current page
    records = db.query(Record).filter(
        and_(*query_conditions)
    ).order_by(
        Record.date.desc()
    ).offset(
        (page - 1) * per_page
    ).limit(per_page).all()
    
    return render_template(
        'main/record_list.html',
        active_page='record_list',
        records=records,
        page=page,
        per_page=per_page,
        total_count=total_count,
        total_pages=total_pages
    )

@record_bp.route('/<int:record_id>/data', methods=('GET',))
@login_required
def get_record_data(record_id):
    """get detailed data of a single record, for edit form"""
    db = get_db()
    
    # query record
    record = db.query(Record).filter(
        Record.id == record_id,
        Record.user_id == g.user.id  # ensure only access own records
    ).first()
    
    if not record:
        return jsonify({'success': False, 'message': 'record not found or no access'}), 404
    
    # convert to JSON format
    record_data = {
        'id': record.id,
        'amount': float(record.amount),
        'type': record.type,
        'date': record.date.strftime('%Y-%m-%d'),
        'category': record.category,
        'description': record.description
    }
    
    return jsonify(record_data)

@record_bp.route('/<int:record_id>/edit', methods=('POST',))
@login_required
def edit_record(record_id):
    """update record"""
    db = get_db()
    
    # query record to edit
    record = db.query(Record).filter(
        Record.id == record_id,
        Record.user_id == g.user.id  # ensure only edit own records
    ).first()
    
    if not record:
        return jsonify({'success': False, 'message': 'record not found or no access'}), 404
    
    try:
        # get form data
        amount = request.form.get('amount')
        category = request.form.get('category')
        date = request.form.get('date')
        description = request.form.get('description', '')
        record_type = request.form.get('type')
        
        # validate data
        if not amount or not category or not date or not record_type:
            return jsonify({'success': False, 'message': 'please fill in all required fields'}), 400
        
        if record_type not in ['income', 'expense']:
            return jsonify({'success': False, 'message': 'invalid transaction type'}), 400
        
        # update record
        record.amount = float(amount)
        record.type = record_type
        record.date = datetime.strptime(date, '%Y-%m-%d').date()
        record.category = category
        record.description = description
        
        db.commit()
        
        return jsonify({'success': True, 'message': 'updated successfully'})
        
    except Exception as e:
        db.rollback()
        return jsonify({'success': False, 'message': f'update failed: {str(e)}'}), 500

@record_bp.route('/<int:record_id>/delete', methods=('POST',))
@login_required
def delete_record(record_id):
    """delete record"""
    db = get_db()
    
    # query record to delete
    record = db.query(Record).filter(
        Record.id == record_id,
        Record.user_id == g.user.id  # ensure only delete own records
    ).first()
    
    if not record:
        return jsonify({'success': False, 'message': 'record not found or no access'}), 404
    
    try:
        # delete record
        db.delete(record)
        db.commit()
        
        return jsonify({'success': True, 'message': 'deleted successfully'})
        
    except Exception as e:
        db.rollback()
        return jsonify({'success': False, 'message': f'delete failed: {str(e)}'}), 500
