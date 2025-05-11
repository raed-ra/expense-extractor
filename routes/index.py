from flask import Blueprint, jsonify
from datetime import datetime, timedelta
from sqlalchemy import func
from models.transaction import Transaction
from db import db

home = Blueprint('home', __name__)

@home.route('/api/financial-overview')
def get_financial_overview():
    # 获取当前日期
    today = datetime.now()
    # 获取本月第一天
    first_day_of_month = today.replace(day=1)
    # 获取上个月第一天
    first_day_of_last_month = (first_day_of_month - timedelta(days=1)).replace(day=1)
    
    # 获取本月收入
    current_month_income = db.session.query(
        func.sum(Transaction.amount)
    ).filter(
        Transaction.type == 'credit',
        Transaction.date >= first_day_of_month.date()
    ).scalar() or 0
    
    # 获取本月支出
    current_month_expenses = db.session.query(
        func.sum(Transaction.amount)
    ).filter(
        Transaction.type == 'debit',
        Transaction.date >= first_day_of_month.date()
    ).scalar() or 0
    
    # 获取上月收入
    last_month_income = db.session.query(
        func.sum(Transaction.amount)
    ).filter(
        Transaction.type == 'credit',
        Transaction.date >= first_day_of_last_month.date(),
        Transaction.date < first_day_of_month.date()
    ).scalar() or 0
    
    # 获取上月支出
    last_month_expenses = db.session.query(
        func.sum(Transaction.amount)
    ).filter(
        Transaction.type == 'debit',
        Transaction.date >= first_day_of_last_month.date(),
        Transaction.date < first_day_of_month.date()
    ).scalar() or 0
    
    # 计算本月余额
    current_month_balance = current_month_income - current_month_expenses
    last_month_balance = last_month_income - last_month_expenses
    
    # 计算环比变化
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
