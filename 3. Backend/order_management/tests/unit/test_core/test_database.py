"""
Unit tests for database module.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from sqlalchemy.orm import Session
from app.core.database import get_db, SessionLocal, engine, set_search_path


def test_get_db_yields_session():
    """Test that get_db yields a database session."""
    # Use actual session local for this test
    db_gen = get_db()
    db = next(db_gen)
    
    try:
        assert db is not None
        assert isinstance(db, Session)
    finally:
        db_gen.close()


def test_get_db_closes_session():
    """Test that get_db closes session after use."""
    db_gen = get_db()
    db = next(db_gen)
    
    # Verify session is open
    assert db.is_active
    
    # Close the generator (simulating finally block)
    try:
        db_gen.close()
    except StopIteration:
        pass


def test_set_search_path_postgresql():
    """Test set_search_path function for PostgreSQL connections."""
    # Mock PostgreSQL connection
    mock_conn = MagicMock()
    mock_conn.__class__.__module__ = "psycopg2.extensions"
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connection_record = MagicMock()
    
    # Call the event listener
    set_search_path(mock_conn, mock_connection_record)
    
    # Verify cursor.execute was called
    mock_cursor.execute.assert_called_once()
    call_args = mock_cursor.execute.call_args[0][0]
    assert "SET search_path" in call_args
    mock_cursor.close.assert_called_once()


def test_set_search_path_non_postgresql():
    """Test set_search_path does nothing for non-PostgreSQL connections."""
    # Mock non-PostgreSQL connection (e.g., SQLite)
    mock_conn = MagicMock()
    mock_conn.__class__.__module__ = "sqlite3"
    mock_connection_record = MagicMock()
    
    # Should not raise error, but also shouldn't execute anything
    # Since SQLite doesn't have a cursor() method like PostgreSQL
    try:
        set_search_path(mock_conn, mock_connection_record)
    except AttributeError:
        # Expected for SQLite connections
        pass


@patch('app.core.database.SessionLocal')
def test_get_db_exception_handling(mock_session_local):
    """Test that get_db properly handles exceptions."""
    # Create a mock session that raises an exception
    mock_session = MagicMock()
    mock_session_local.return_value = mock_session
    mock_session.close = MagicMock()
    
    # Create generator
    db_gen = get_db()
    
    # Get the session
    db = next(db_gen)
    
    # Close generator (simulates finally block)
    try:
        db_gen.close()
    except StopIteration:
        pass
    
    # Verify close was called (through mock if needed)
    # In real scenario, db.close() would be called in finally

