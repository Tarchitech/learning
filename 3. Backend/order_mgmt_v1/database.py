"""
Database connection and session management.

This module handles:
- SQLAlchemy engine creation
- Base class for ORM models
- Table creation on initialization
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get database URL from environment variable
# If DATABASE_URL is not set, it will raise an error
database_url = os.getenv('DATABASE_URL')

if not database_url:
    raise ValueError(
        "DATABASE_URL environment variable is not set. "
        "Please create a .env file based on .env.example and set your database connection string."
    )

# Create SQLAlchemy engine using the connection string from .env
engine = create_engine(database_url)


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
