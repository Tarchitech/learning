"""
Order ORM model.
"""
from datetime import datetime
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Index, CheckConstraint
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Order(BaseModel):
    """Order model representing orders table."""
    
    __tablename__ = "orders"
    __table_args__ = (
        Index("idx_orders_user_id", "user_id"),
        CheckConstraint(
            "status IN ('pending', 'paid', 'shipped', 'cancelled')",
            name="orders_status_check"
        ),
        {"schema": "tony"},
    )
    
    user_id = Column(Integer, ForeignKey("tony.users.id"), nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.utcnow, nullable=True)
    
    # Relationships
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    user = relationship("User", foreign_keys=[user_id])
    
    def __repr__(self) -> str:
        return f"<Order(id={self.id}, user_id={self.user_id}, status='{self.status}')>"
