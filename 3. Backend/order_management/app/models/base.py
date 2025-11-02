"""
Base model class with common fields.
"""
from sqlalchemy import Column, Integer
from app.core.database import Base


class BaseModel(Base):
    """Abstract base model with common fields."""
    
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True)

