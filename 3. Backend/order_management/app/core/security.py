"""
Security utilities for validation and data protection.
"""
from pydantic import EmailStr, TypeAdapter


def validate_email(email: str) -> bool:
    """
    Validate email format using Pydantic v2 EmailStr validator.
    
    Args:
        email: Email address to validate
        
    Returns:
        bool: True if email is valid, False otherwise
    """
    try:
        # In Pydantic v2, use TypeAdapter to validate EmailStr
        email_adapter = TypeAdapter(EmailStr)
        email_adapter.validate_python(email)
        return True
    except Exception:
        return False


def sanitize_string(input_str: str) -> str:
    """
    Sanitize string input to prevent injection attacks.
    
    Args:
        input_str: String to sanitize
        
    Returns:
        str: Sanitized string
    """
    # Remove potential SQL injection patterns
    dangerous_patterns = ["';", "--", "/*", "*/", "xp_", "sp_"]
    sanitized = input_str
    for pattern in dangerous_patterns:
        sanitized = sanitized.replace(pattern, "")
    return sanitized.strip()


ORDER_STATUSES = ["pending", "paid", "shipped", "cancelled"]


def validate_order_status(status: str) -> bool:
    """
    Validate order status value.
    
    Args:
        status: Order status to validate
        
    Returns:
        bool: True if status is valid, False otherwise
    """
    return status.lower() in ORDER_STATUSES

