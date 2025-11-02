"""
User ORM model.
"""
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from app.models.base import BaseModel


class User(BaseModel):
    """User model representing users table."""
    
    __tablename__ = "users"
    __table_args__ = ({"schema": "tony"},)
    
    email = Column(String, unique=True, nullable=False, index=True)
    full_name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=True)
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, email='{self.email}', full_name='{self.full_name}')>"
