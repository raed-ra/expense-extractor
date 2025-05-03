# models/db.py

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session

# Define your DB URL (SQLite in this case)
DATABASE_URL = "sqlite:///expensemanager.db"

# Create engine (the connection to the DB)
engine = create_engine(DATABASE_URL, echo=True)

# Create base model class for all ORM models to inherit
Base = declarative_base()

# Create a session factory (for querying, inserting)
SessionLocal = scoped_session(sessionmaker(bind=engine))
