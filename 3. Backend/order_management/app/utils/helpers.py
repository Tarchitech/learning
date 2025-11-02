"""
Helper functions for common operations.
"""
from datetime import datetime
from typing import Optional


def parse_iso_date(date_str: Optional[str]) -> Optional[datetime]:
    """
    Parse ISO 8601 date string to datetime object.
    
    Args:
        date_str: ISO 8601 formatted date string
        
    Returns:
        Optional[datetime]: Parsed datetime object or None
    """
    if not date_str:
        return None
    
    try:
        # Try parsing with timezone
        return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    except ValueError:
        try:
            # Try parsing without timezone
            return datetime.fromisoformat(date_str)
        except ValueError:
            raise ValueError(f"Invalid date format: {date_str}. Expected ISO 8601 format.")

