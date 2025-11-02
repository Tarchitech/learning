"""
User Pydantic schemas for request/response validation.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr


class UserBase(BaseModel):
    """Base user schema with common fields."""
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=255)


class UserCreate(UserBase):
    """Schema for creating a user."""
    pass


class UserUpdate(BaseModel):
    """Schema for updating a user."""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, min_length=1, max_length=255)
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "newemail@example.com",
                "full_name": "Jane Doe"
            }
        }


class UserResponse(UserBase):
    """Schema for user response."""
    id: int
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "email": "user@example.com",
                "full_name": "John Doe",
                "created_at": "2024-01-10T08:00:00Z"
            }
        }


class UserListResponse(BaseModel):
    """Schema for user list response."""
    items: list[UserResponse]
    total: int
    limit: int
    offset: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "items": [
                    {
                        "id": 1,
                        "email": "user@example.com",
                        "full_name": "John Doe",
                        "created_at": "2024-01-10T08:00:00Z"
                    }
                ],
                "total": 100,
                "limit": 20,
                "offset": 0
            }
        }

