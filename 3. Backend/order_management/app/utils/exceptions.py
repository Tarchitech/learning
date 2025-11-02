"""
Custom exception classes for the application.
"""


class OrderNotFoundError(Exception):
    """Raised when an order is not found."""
    pass


class ProductNotFoundError(Exception):
    """Raised when a product is not found."""
    pass


class UserNotFoundError(Exception):
    """Raised when a user is not found."""
    pass


class ValidationError(Exception):
    """Raised when input validation fails."""
    pass


class DuplicateEmailError(Exception):
    """Raised when attempting to create a user with an existing email."""
    pass

