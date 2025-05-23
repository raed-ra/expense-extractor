
# /models/shared_report.py
from sqlalchemy import Column, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from db import Base
from datetime import datetime

class SharedReport(Base):
    __tablename__ = 'shared_reports'

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('users.id'))
    recipient_id = Column(Integer, ForeignKey('users.id'))
    filter_params = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", foreign_keys=[owner_id])
    recipient = relationship("User", foreign_keys=[recipient_id])
