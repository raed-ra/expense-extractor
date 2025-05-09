from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey
from db import Base
from datetime import datetime

class SharedView(Base):
    __tablename__ = 'shared_views'

    id = Column(Integer, primary_key=True)
    shared_report_id = Column(Integer, ForeignKey('shared_reports.id'))
    viewer_id = Column(Integer, ForeignKey('users.id'))
    viewed_at = Column(DateTime, default=datetime.utcnow)
    notified_owner = Column(Boolean, default=False)
