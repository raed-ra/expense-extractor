from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Date

db = SQLAlchemy()

class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String, nullable=False)
    uploaded_at = db.Column(db.DateTime, nullable=False)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String, nullable=False)
    date = db.Column(Date, nullable=True)  
    type = db.Column(db.String, nullable=True)  
    upload_id = db.Column(db.Integer, db.ForeignKey('upload.id'))
