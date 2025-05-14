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
    """获取用户的财务概览数据"""
    db = get_db()
    
    # 获取当前月份和上个月的日期范围
    today = datetime.today()
    current_month_start = datetime(today.year, today.month, 1)
    
    # 上个月的开始日期
    if today.month == 1:
        previous_month_start = datetime(today.year - 1, 12, 1)
    else:
        previous_month_start = datetime(today.year, today.month - 1, 1)


    # 计算当前月份支出和收入
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
    
    
    # 计算上个月支出和收入
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
    
    
    
    
    # 获取最近10笔交易
    recent_transactions = db.query(Transaction).filter(
        Transaction.user_id == g.user.id
    ).order_by(Transaction.date.desc()).limit(10).all()
    
    # 计算收入和支出变化百分比
    income_change = calculate_percentage_change(previous_month_income, current_month_income)
    expense_change = calculate_percentage_change(previous_month_expenses, current_month_expenses)
    
    # 计算当前和上个月的余额
    current_balance = float(current_month_income) - float(current_month_expenses)
    previous_balance = float(previous_month_income) - float(previous_month_expenses)
    balance_change = calculate_percentage_change(previous_balance, current_balance)
    
    # 构建符合前端期望的响应数据格式
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
    
    print("API响应数据:", response_data)
    return jsonify(response_data)

def calculate_percentage_change(old_value, new_value):
    """计算百分比变化"""
    if old_value == 0:
        if new_value > 0:
            return 100
        else:
            return 0
    else:
        return ((new_value - old_value) / old_value) * 100 
    


