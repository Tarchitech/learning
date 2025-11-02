"""
Unit tests for helper functions.
"""
import pytest
from datetime import datetime
from app.utils.helpers import parse_iso_date


def test_parse_iso_date_with_timezone():
    """Test parsing ISO date string with timezone."""
    date_str = "2024-01-15T10:30:00Z"
    result = parse_iso_date(date_str)
    assert result is not None
    assert isinstance(result, datetime)
    assert result.year == 2024
    assert result.month == 1
    assert result.day == 15


def test_parse_iso_date_with_timezone_offset():
    """Test parsing ISO date string with timezone offset."""
    date_str = "2024-01-15T10:30:00+00:00"
    result = parse_iso_date(date_str)
    assert result is not None
    assert isinstance(result, datetime)
    assert result.year == 2024
    assert result.month == 1
    assert result.day == 15


def test_parse_iso_date_without_timezone():
    """Test parsing ISO date string without timezone."""
    date_str = "2024-01-15T10:30:00"
    result = parse_iso_date(date_str)
    assert result is not None
    assert isinstance(result, datetime)
    assert result.year == 2024
    assert result.month == 1
    assert result.day == 15


def test_parse_iso_date_none():
    """Test parsing None date string."""
    result = parse_iso_date(None)
    assert result is None


def test_parse_iso_date_empty_string():
    """Test parsing empty date string."""
    result = parse_iso_date("")
    assert result is None


def test_parse_iso_date_invalid_format():
    """Test parsing invalid date format."""
    with pytest.raises(ValueError, match="Invalid date format"):
        parse_iso_date("invalid-date-format")


def test_parse_iso_date_invalid_date():
    """Test parsing invalid date."""
    with pytest.raises(ValueError, match="Invalid date format"):
        parse_iso_date("2024-13-45T99:99:99")


def test_parse_iso_date_date_only():
    """Test parsing date-only string."""
    date_str = "2024-01-15"
    result = parse_iso_date(date_str)
    assert result is not None
    assert isinstance(result, datetime)
    assert result.year == 2024
    assert result.month == 1
    assert result.day == 15


def test_parse_iso_date_with_milliseconds():
    """Test parsing ISO date with milliseconds."""
    date_str = "2024-01-15T10:30:00.123Z"
    result = parse_iso_date(date_str)
    assert result is not None
    assert isinstance(result, datetime)

