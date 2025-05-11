from flask import Blueprint, render_template, g, request, jsonify
from datetime import datetime
from flask_login import login_required

from db import get_db
from models import Transaction

flow_bp = Blueprint('flow', __name__, url_prefix='/flow')

@flow_bp.route('/')
@login_required
def index():
    db = get_db()
    transactions = db.query(Transaction).filter_by(user_id=g.user.id).order_by(Transaction.date.desc()).all()
    return render_template(
        'main/flow.html',
        transactions=transactions,
        active_page='flow' 
    )

@flow_bp.route('/<int:transaction_id>/edit', methods=['POST'])
@login_required
def edit_transaction(transaction_id):
    db = get_db()
    txn = db.query(Transaction).filter_by(id=transaction_id, user_id=g.user.id).first()

    if not txn:
        return jsonify(success=False, message="Transaction not found"), 404

    # Update fields from the form
    txn.date = datetime.strptime(request.form.get("date"), "%Y-%m-%d").date()
    txn.type = request.form.get("type")
    txn.credit_type = request.form.get("credit_type")
    txn.category = request.form.get("category")
    txn.description = request.form.get("description")
    txn.amount = float(request.form.get("amount") or 0)

    db.commit()
    return jsonify(success=True)
