"""
Database connection and session management.
"""
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy.pool import NullPool
from app.core.config import settings

# Create database engine
engine = create_engine(
    settings.database_url,
    poolclass=NullPool,  # For Neon.tech connection pooling
    echo=settings.DEBUG,
    future=True,
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()


def get_db() -> Session:
    """
    Dependency function to get database session.
    
    Yields:
        Session: Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@event.listens_for(engine, "connect")
def set_search_path(dbapi_conn, connection_record):
    """Set search path to specified schema."""
    # Only set search path for PostgreSQL connections
    if dbapi_conn.__class__.__module__.startswith("psycopg"):
        cursor = dbapi_conn.cursor()
        cursor.execute(f'SET search_path TO {settings.DB_SCHEMA}')
        cursor.close()

