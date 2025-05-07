from flask import Blueprint, request, jsonify, render_template, Response
from flask_login import login_required, current_user
from models.transaction import Transaction
from sqlalchemy import and_
from dateutil import parser as date_parser
from db import get_db
from io import StringIO
import csv 

def build_filtered_query(db, user, params):
    
    # Only return data if at least one filter is applied - deactivate this for now
    #if not (from_date or to_date or category or txn_type or amount_filter #or description_keyword):
    #return jsonify([])  # return an empty list
    query = db.query(Transaction).filter(Transaction.user_id == user.id)

    from_date = params.get('from')
    to_date = params.get('to')
    category = params.get('category')
    txn_type = params.get('type')
    amount_filter = params.get('amount_filter')
    description_keyword = params.get('description')

    if from_date and to_date:
        try:
            start = date_parser.parse(from_date).date()
            end = date_parser.parse(to_date).date()
            query = query.filter(Transaction.date.between(start, end))
        except Exception:
            pass

    if category and category != '__all__':
        query = query.filter(Transaction.category == category)

    if txn_type and txn_type != '__all__':
        query = query.filter(Transaction.type == txn_type)

    if amount_filter:
        try:
            value = float(amount_filter)
            query = query.filter(Transaction.amount >= value)
        except Exception:
            pass

    if description_keyword:
        query = query.filter(Transaction.description.ilike(f"%{description_keyword}%"))

    return query


report_bp = Blueprint('report', __name__,url_prefix='/report')

@report_bp.route('/data', methods=['GET'])
@login_required
def report_data():
    db = get_db()
    query = build_filtered_query(db, current_user, request.args)
    results = query.order_by(Transaction.date).all()

    return jsonify([{
        "date": t.date.isoformat(),
        "description": t.description,
        "amount": t.amount,
        "type": t.type,
        "category": t.category
    } for t in results])



@report_bp.route('/', methods=['GET'])
@login_required
def report():
    db = get_db()
    # Initial page render
    categories = [
        c[0] for c in db.query(Transaction.category).distinct().filter(Transaction.user_id == current_user.id)]
    
    # Also get all distinct dates for this user
    transaction_dates = [
    t[0].isoformat()
    for t in db.query(Transaction.date)
              .distinct()
              .filter(Transaction.user_id == current_user.id)]
  
    return render_template(
    'main/report.html',
    active_page='report',
    categories=categories,
    transaction_dates=transaction_dates
)

@report_bp.route('/export', methods=['GET'])
@login_required
def export_csv():
    db = get_db()
    query = build_filtered_query(db, current_user, request.args)
    results = query.order_by(Transaction.date).all()

    si = StringIO()
    writer = csv.writer(si)
    writer.writerow(['Date', 'Description', 'Amount', 'Type', 'Category'])
    for t in results:
        writer.writerow([t.date, t.description, t.amount, t.type, t.category])

    return Response(
        si.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=transactions.csv"}
    )
