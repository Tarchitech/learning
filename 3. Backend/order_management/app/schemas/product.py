"""
Product Pydantic schemas for request/response validation.
"""
from typing import Optional
from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    """Base product schema with common fields."""
    name: str = Field(..., min_length=1, max_length=255)
    price_cents: int = Field(..., ge=0, description="Price in cents")


class ProductCreate(ProductBase):
    """Schema for creating a product."""
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Product A",
                "price_cents": 1999
            }
        }


class ProductUpdate(BaseModel):
    """Schema for updating a product."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    price_cents: Optional[int] = Field(None, ge=0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Updated Product A",
                "price_cents": 2499
            }
        }


class ProductResponse(ProductBase):
    """Schema for product response."""
    id: int
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Product A",
                "price_cents": 1999
            }
        }


class ProductListResponse(BaseModel):
    """Schema for product list response."""
    items: list[ProductResponse]
    total: int
    limit: int
    offset: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "items": [
                    {
                        "id": 1,
                        "name": "Product A",
                        "price_cents": 1999
                    }
                ],
                "total": 50,
                "limit": 20,
                "offset": 0
            }
        }

