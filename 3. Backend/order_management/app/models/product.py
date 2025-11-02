"""
Product ORM model.
"""
from sqlalchemy import Column, String, Integer, CheckConstraint
from app.models.base import BaseModel


class Product(BaseModel):
    """Product model representing products table."""
    
    __tablename__ = "products"
    __table_args__ = (
        CheckConstraint("price_cents >= 0", name="products_price_cents_check"),
        {"schema": "tony"},
    )
    
    name = Column(String, nullable=False)
    price_cents = Column(Integer, nullable=False)
    
    def __repr__(self) -> str:
        return f"<Product(id={self.id}, name='{self.name}', price_cents={self.price_cents})>"
