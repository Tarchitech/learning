"""
Product repository for data access operations.
"""
from typing import Optional
from sqlalchemy.orm import Session
from app.models.product import Product
from app.repositories.base import BaseRepository


class ProductRepository(BaseRepository[Product]):
    """Product repository with product-specific operations."""
    
    def __init__(self, db: Session):
        """Initialize product repository."""
        super().__init__(Product, db)

