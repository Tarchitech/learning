"""
Order Pydantic schemas for request/response validation.
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class OrderItemBase(BaseModel):
    """Base order item schema."""
    product_id: int = Field(..., description="Product ID", example=1)
    quantity: int = Field(..., gt=0, description="Quantity", example=2)


class OrderItemCreate(OrderItemBase):
    """Schema for creating an order item."""
    pass


class OrderItemResponse(OrderItemBase):
    """Schema for order item response."""
    id: int = Field(..., description="Order item ID")
    price_cents_at_purchase: int = Field(..., description="Total price for this product (quantity * unit_price) in cents")
    product_name: Optional[str] = Field(None, description="Product name")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "product_id": 1,
                "quantity": 1,
                "price_cents_at_purchase": 249999,
                "product_name": "MacBook Pro 16\""
            }
        }


class OrderBase(BaseModel):
    """Base order schema."""
    user_id: int = Field(..., description="User ID")
    status: str = Field(default="pending", description="Order status")


class OrderCreate(OrderBase):
    """Schema for creating an order."""
    items: List[OrderItemCreate] = Field(..., min_items=1, description="List of order items")
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 1,
                "status": "pending",
                "items": [
                    {"product_id": 1, "quantity": 2},
                    {"product_id": 2, "quantity": 1}
                ]
            }
        }


class OrderUpdate(BaseModel):
    """Schema for updating an order."""
    status: str = Field(..., description="Order status")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "paid"
            }
        }


class OrderResponse(OrderBase):
    """Schema for order response (used for list and create)."""
    order_id: int = Field(..., description="Order ID")
    created_at: Optional[datetime] = None
    items: List[OrderItemResponse] = []
    total_amount_cents: int = Field(default=0, description="Total amount in cents")
    total_quantity: int = Field(default=0, description="Total quantity")
    user_name: Optional[str] = Field(None, description="User full name")
    
    class Config:
        from_attributes = False
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "order_id": 1,
                "user_id": 1,
                "status": "paid",
                "created_at": "2024-01-16T10:30:00Z",
                "user_name": "John Joe",
                "items": [
                    {
                        "product_id": 1,
                        "quantity": 1,
                        "price_cents_at_purchase": 249999,
                        "product_name": "MacBook Pro 16\""
                    }
                ],
                "total_amount_cents": 279998,
                "total_quantity": 2
            }
        }


class OrderListResponse(BaseModel):
    """Schema for order list response."""
    orders: List[OrderResponse] = Field(..., description="List of orders")
    limit: int
    offset: int
    total_amount_cents: int = Field(default=0, description="Total amount across all results")
    total_quantity: int = Field(default=0, description="Total quantity across all results")
    
    class Config:
        json_schema_extra = {
            "example": {
                "orders": [
                    {
                        "order_id": 1,
                        "user_id": 1,
                        "user_name": "John Joe",
                        "status": "paid",
                        "created_at": "2024-01-16T10:30:00Z",
                        "items": [
                            {
                                "product_id": 1,
                                "quantity": 1,
                                "price_cents_at_purchase": 249999,
                                "product_name": "MacBook Pro 16\""
                            }
                        ],
                        "total_amount_cents": 279998,
                        "total_quantity": 2
                    }
                ],
                "limit": 20,
                "offset": 0,
                "total_amount_cents": 689992,
                "total_quantity": 8
            }
        }


class OrderStatusUpdateResponse(BaseModel):
    """Schema for order status update response."""
    order_id: int = Field(..., description="Order ID")
    user_id: int = Field(..., description="User ID")
    status: str = Field(..., description="Order status")
    created_at: Optional[datetime] = Field(None, description="Order creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Order update timestamp")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "order_id": 1,
                "user_id": 1,
                "status": "paid",
                "created_at": "2024-01-15T10:30:00Z",
                "updated_at": "2024-01-15T11:00:00Z"
            }
        }

