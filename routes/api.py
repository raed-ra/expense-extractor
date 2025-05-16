from flask import Blueprint, jsonify, g
from flask_login import login_required
from sqlalchemy import func
from datetime import datetime, timedelta
from db import get_db
from models.transaction import Transaction

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/financial-overview', methods=['GET'])
@login_required
def financial_overview():
    """get user's financial overview data"""
    db = get_db()
    
    # get current month and last month date range
    today = datetime.today()
    current_month_start = datetime(today.year, today.month, 1)
    
    # last month start date
    if today.month == 1:
        previous_month_start = datetime(today.year - 1, 12, 1)
    else:
        previous_month_start = datetime(today.year, today.month - 1, 1)


    # calculate current month expenses and income
    current_month_expenses = db.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == g.user.id,
        Transaction.type == 'expense',
        Transaction.date >= current_month_start,
        Transaction.date < today + timedelta(days=1)
    ).scalar() or 0

    current_month_income = db.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == g.user.id,
        Transaction.type == 'income',
        Transaction.date >= current_month_start,
        Transaction.date < today + timedelta(days=1)
    ).scalar() or 0
    
    
    # calculate last month expenses and income
    previous_month_expenses = db.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == g.user.id,
        Transaction.type == 'expense',
        Transaction.date >= previous_month_start,
        Transaction.date < current_month_start
    ).scalar() or 0

    previous_month_income = db.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == g.user.id,
        Transaction.type == 'income',
        Transaction.date >= previous_month_start,
        Transaction.date < current_month_start
    ).scalar() or 0
    
    
    
    
    # get recent 10 transactions
    recent_transactions = db.query(Transaction).filter(
        Transaction.user_id == g.user.id
    ).order_by(Transaction.date.desc()).limit(10).all()
    
    # calculate income and expenses change percentage
    income_change = calculate_percentage_change(previous_month_income, current_month_income)
    expense_change = calculate_percentage_change(previous_month_expenses, current_month_expenses)
    
    # calculate current and last month balance
    current_balance = float(current_month_income) - float(current_month_expenses)
    previous_balance = float(previous_month_income) - float(previous_month_expenses)
    balance_change = calculate_percentage_change(previous_balance, current_balance)
    
    # build response data format as expected by frontend
    response_data = {
        'income': {
            'amount': float(current_month_income),
            'change': float(income_change)
        },
        'expenses': {
            'amount': float(current_month_expenses),
            'change': float(expense_change)
        },
        'balance': {
            'amount': current_balance,
            'change': float(balance_change)
        },
        'recent_transactions': [
            {
                'date': transaction.date.strftime('%Y-%m-%d'),
                'category': transaction.category,
                'type': transaction.type,
                'amount': float(transaction.amount),
                'description': transaction.description
            } for transaction in recent_transactions
        ]
    }
    
    print("API response data:", response_data)
    return jsonify(response_data)

def calculate_percentage_change(old_value, new_value):
    """calculate percentage change"""
    if old_value == 0:
        if new_value > 0:
            return 100
        else:
            return 0
    else:
        return ((new_value - old_value) / old_value) * 100 
    


