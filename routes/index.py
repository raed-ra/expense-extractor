from flask import Blueprint, jsonify
from datetime import datetime, timedelta
from sqlalchemy import func
from models.transaction import Transaction
from db import db

home = Blueprint('home', __name__)

@home.route('/api/financial-overview')
def get_financial_overview():
    # get date
    today = datetime.now()
    # get first day of month
    first_day_of_month = today.replace(day=1)
    # get first day of last month
    first_day_of_last_month = (first_day_of_month - timedelta(days=1)).replace(day=1)
    
    # get current month income
    current_month_income = db.session.query(
        func.sum(Transaction.amount)
    ).filter(
        Transaction.type == 'credit',
        Transaction.date >= first_day_of_month.date()
    ).scalar() or 0
    
    # get current month expenses
    current_month_expenses = db.session.query(
        func.sum(Transaction.amount)
    ).filter(
        Transaction.type == 'debit',
        Transaction.date >= first_day_of_month.date()
    ).scalar() or 0
    
    # get last month income
    last_month_income = db.session.query(
        func.sum(Transaction.amount)
    ).filter(
        Transaction.type == 'credit',
        Transaction.date >= first_day_of_last_month.date(),
        Transaction.date < first_day_of_month.date()
    ).scalar() or 0
    
    # get last month expenses
    last_month_expenses = db.session.query(
        func.sum(Transaction.amount)
    ).filter(
        Transaction.type == 'debit',
        Transaction.date >= first_day_of_last_month.date(),
        Transaction.date < first_day_of_month.date()
    ).scalar() or 0
    
    # calculate current month balance
    current_month_balance = current_month_income - current_month_expenses
    last_month_balance = last_month_income - last_month_expenses
    
    # calculate month-over-month change
    income_change = ((current_month_income - last_month_income) / last_month_income * 100) if last_month_income else 0
    expenses_change = ((current_month_expenses - last_month_expenses) / last_month_expenses * 100) if last_month_expenses else 0
    balance_change = ((current_month_balance - last_month_balance) / last_month_balance * 100) if last_month_balance else 0
    
    return jsonify({
        'income': {
            'amount': float(current_month_income),
            'change': float(income_change)
        },
        'expenses': {
            'amount': float(current_month_expenses),
            'change': float(expenses_change)
        },
        'balance': {
            'amount': float(current_month_balance),
            'change': float(balance_change)
        }
    })
