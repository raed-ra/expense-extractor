from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Date, DateTime
from datetime import datetime
from db import Base

class Record(Base):
    __tablename__ = 'records'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    category = Column(String(50), nullable=False)  #category type,such as Dining、Salary
    type = Column(String(20), nullable=False)  # 'income' or 'expense'
    amount = Column(Numeric(10, 2), nullable=False)  # amount,required
    date = Column(Date, nullable=False)             # date,required
    description = Column(String(255))               # description,optional
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)