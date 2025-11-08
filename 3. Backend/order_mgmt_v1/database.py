"""
Database connection and session management.

This module handles:
- SQLAlchemy engine creation
- Base class for ORM models
- Table creation on initialization
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine('postgresql://db_user:db_password@ep-jolly-feather-adyuujqy-pooler.c-2.us-east-1.aws.neon.tech:5432/postgres')

# ============================================================================
# Get Database Session
# ============================================================================
def get_db():
    """
    Create and return a new database session.
    
    Each database operation should use a new session. This function
    creates a session directly from the engine.
    
    Returns:
        Session: A new SQLAlchemy database session
    """
    return Session(engine)
