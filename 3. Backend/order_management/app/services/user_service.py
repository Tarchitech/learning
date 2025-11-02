"""
User service for business logic operations.
"""
from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserListResponse
from app.repositories.user_repository import UserRepository
from app.utils.exceptions import UserNotFoundError, DuplicateEmailError, ValidationError
from app.core.security import validate_email


class UserService:
    """User service with business logic."""
    
    def __init__(self, db: Session):
        """
        Initialize user service.
        
        Args:
            db: Database session
        """
        self.repository = UserRepository(db)
        self.db = db
    
    def get_user(self, user_id: int) -> UserResponse:
        """
        Get user by ID.
        
        Args:
            user_id: User ID
            
        Returns:
            UserResponse: User response
            
        Raises:
            UserNotFoundError: If user not found
        """
        user = self.repository.get(user_id)
        if not user:
            raise UserNotFoundError(f"User with ID {user_id} not found")
        return UserResponse.model_validate(user)
    
    def get_users(
        self,
        skip: int = 0,
        limit: int = 20,
    ) -> UserListResponse:
        """
        Get all users with pagination.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            UserListResponse: List of users
        """
        users, total = self.repository.get_all(skip=skip, limit=limit)
        return UserListResponse(
            items=[UserResponse.model_validate(user) for user in users],
            total=total,
            limit=limit,
            offset=skip,
        )
    
    def update_user(self, user_id: int, user_update: UserUpdate) -> UserResponse:
        """
        Update user information.
        
        Args:
            user_id: User ID
            user_update: User update data
            
        Returns:
            UserResponse: Updated user
            
        Raises:
            UserNotFoundError: If user not found
            DuplicateEmailError: If email already exists
            ValidationError: If validation fails
        """
        # Check if user exists
        user = self.repository.get(user_id)
        if not user:
            raise UserNotFoundError(f"User with ID {user_id} not found")
        
        # Prepare update data
        update_data = {}
        
        if user_update.email is not None:
            if not validate_email(user_update.email):
                raise ValidationError("Invalid email format")
            
            # Check for duplicate email
            if self.repository.email_exists(user_update.email, exclude_id=user_id):
                raise DuplicateEmailError(f"Email {user_update.email} already exists")
            update_data["email"] = user_update.email
        
        if user_update.full_name is not None:
            if not user_update.full_name.strip():
                raise ValidationError("Full name cannot be empty")
            update_data["full_name"] = user_update.full_name
        
        if not update_data:
            raise ValidationError("At least one field must be provided for update")
        
        # Update user
        updated_user = self.repository.update(user_id, update_data)
        if not updated_user:
            raise UserNotFoundError(f"User with ID {user_id} not found")
        
        return UserResponse.model_validate(updated_user)

