from sqlalchemy import Column, Integer, String, DateTime, Date, Time, Numeric, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from db import Base  # Adjust if using a package structure (e.g., from ..db import Base)

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)

    # Main fields
    type = Column(String(20), nullable=True)               # 'income' or 'expense'
    credit_type = Column(String(20), nullable=True)        # 'debit' or 'credit'
    amount = Column(Numeric(10, 2), nullable=False)         # Monetary value with 2 decimal places
    category = Column(String(50), nullable=True)            # Free-text category
    date = Column(Date, nullable=False)                     # Date of transaction
    time = Column(Time, nullable=True)                      # Optional time
    description = Column(String(255), nullable=True)              # Description of transaction

    # Foreign keys
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    upload_id = Column(Integer, ForeignKey('uploads.id'), nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="transactions")
    upload = relationship("Upload", back_populates="transactions", lazy='joined')

    __table_args__ = (
        Index('idx_transaction_user_date', 'user_id', 'date'),
        Index('idx_transaction_category', 'category'),
    )
