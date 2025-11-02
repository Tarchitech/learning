"""
OrderItem ORM model.
"""
from sqlalchemy import Column, Integer, ForeignKey, CheckConstraint, Index
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class OrderItem(BaseModel):
    """OrderItem model representing order_items table."""
    
    __tablename__ = "order_items"
    __table_args__ = (
        Index("idx_order_items_order_id", "order_id"),
        CheckConstraint("quantity > 0", name="order_items_quantity_check"),
        {"schema": "tony"},
    )
    
    order_id = Column(Integer, ForeignKey("tony.orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("tony.products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price_cents_at_purchase = Column(Integer, nullable=False)
    
    # Relationships
    order = relationship("Order", back_populates="items")
    product = relationship("Product", foreign_keys=[product_id])
    
    def __repr__(self) -> str:
        return (
            f"<OrderItem(id={self.id}, order_id={self.order_id}, "
            f"product_id={self.product_id}, quantity={self.quantity})>"
        )
