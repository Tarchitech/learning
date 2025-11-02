"""
User repository for data access operations.
"""
from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """User repository with user-specific operations."""
    
    def __init__(self, db: Session):
        """Initialize user repository."""
        super().__init__(User, db)
    
    def get_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email.
        
        Args:
            email: User email
            
        Returns:
            Optional[User]: User or None if not found
        """
        return self.db.query(User).filter(User.email == email).first()
    
    def email_exists(self, email: str, exclude_id: Optional[int] = None) -> bool:
        """
        Check if email already exists.
        
        Args:
            email: Email to check
            exclude_id: User ID to exclude from check
            
        Returns:
            bool: True if email exists, False otherwise
        """
        query = self.db.query(User).filter(User.email == email)
        if exclude_id:
            query = query.filter(User.id != exclude_id)
        return query.first() is not None

