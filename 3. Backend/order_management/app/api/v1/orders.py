"""
Order-related API endpoints.
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.services.order_service import OrderService
from app.schemas.order import (
    OrderCreate, 
    OrderUpdate, 
    OrderResponse, 
    OrderListResponse,
    OrderStatusUpdateResponse
)
from app.utils.exceptions import (
    OrderNotFoundError,
    UserNotFoundError,
    ProductNotFoundError,
    ValidationError,
)

router = APIRouter()


@router.get(
    "/orders",
    response_model=OrderListResponse,
    summary="List orders",
    description="Retrieve a list of orders with optional filtering by status, user, date range, or product. Returns paginated results with aggregation totals.",
    tags=["orders"],
    responses={
        200: {
            "description": "Successful response with list of orders",
            "content": {
                "application/json": {
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
                                        "id": 1,
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
            }
        },
        400: {
            "description": "Invalid query parameters",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid status value. Must be one of: pending, paid, shipped, cancelled",
                        "code": "INVALID_STATUS"
                    }
                }
            }
        },
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "An internal error occurred",
                        "code": "INTERNAL_ERROR"
                    }
                }
            }
        }
    }
)
def list_orders(
    status: Optional[str] = Query(None, description="Filter by order status", example="paid"),
    user_id: Optional[int] = Query(None, description="Filter by user ID", example=1),
    start_date: Optional[str] = Query(None, description="Filter orders from this date (ISO 8601)", example="2024-01-01T00:00:00Z"),
    end_date: Optional[str] = Query(None, description="Filter orders until this date (ISO 8601)", example="2024-12-31T23:59:59Z"),
    product_id: Optional[int] = Query(None, description="Filter orders containing this product ID", example=1),
    limit: int = Query(20, ge=1, le=100, description="Number of results per page"),
    offset: int = Query(0, ge=0, description="Number of results to skip"),
    db: Session = Depends(get_db),
) -> OrderListResponse:
    """
    Retrieve orders with optional filtering.
    
    Supports filtering by status, user, date range, and product.
    Returns paginated results with aggregation totals.
    """
    try:
        service = OrderService(db)
        return service.get_orders(
            status=status,
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
            product_id=product_id,
            skip=offset,
            limit=limit,
        )
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Log the error for debugging
        import logging
        logging.error(f"Error in list_orders: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An internal error occurred: {str(e)}")


@router.post(
    "/orders",
    response_model=OrderResponse,
    status_code=201,
    summary="Create order",
    description="Create a new order with items. Validates user and products exist, and captures product prices at purchase time.",
    tags=["orders"],
    responses={
        201: {
            "description": "Order created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "user_id": 1,
                        "status": "pending",
                        "created_at": "2024-01-15T10:30:00Z",
                        "items": [
                            {
                                "id": 1,
                                "product_id": 1,
                                "quantity": 2,
                                "price_cents_at_purchase": 1999
                            }
                        ],
                        "total_amount_cents": 3998,
                        "total_quantity": 2
                    }
                }
            }
        },
        400: {
            "description": "Validation error or invalid data",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid status. Must be one of: pending, paid, shipped, cancelled",
                        "code": "VALIDATION_ERROR"
                    }
                }
            }
        },
        404: {
            "description": "User or product not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "User with ID 1 not found",
                        "code": "NOT_FOUND"
                    }
                }
            }
        }
    }
)
def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
) -> OrderResponse:
    """
    Create a new order with items.
    
    Validates that the user exists and all products exist.
    Captures product prices at the time of purchase.
    """
    try:
        service = OrderService(db)
        return service.create_order(order_data)
    except (UserNotFoundError, ProductNotFoundError) as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An internal error occurred")


@router.patch(
    "/orders/{order_id}",
    response_model=OrderStatusUpdateResponse,
    summary="Update order status",
    description="Update the status of an existing order. Valid status values: pending, paid, shipped, cancelled.",
    tags=["orders"],
    responses={
        200: {
            "description": "Order updated successfully",
            "content": {
                "application/json": {
                    "example": {
                        "order_id": 1,
                        "user_id": 1,
                        "status": "paid",
                        "created_at": "2024-01-15T10:30:00Z",
                        "updated_at": "2024-01-15T11:00:00Z"
                    }
                }
            }
        },
        400: {
            "description": "Invalid status value",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid status. Must be one of: pending, paid, shipped, cancelled",
                        "code": "VALIDATION_ERROR"
                    }
                }
            }
        },
        404: {
            "description": "Order not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Order with ID 1 not found",
                        "code": "NOT_FOUND"
                    }
                }
            }
        }
    }
)
def update_order_status(
    order_id: int,
    order_update: OrderUpdate,
    db: Session = Depends(get_db),
) -> OrderStatusUpdateResponse:
    """
    Update order status.
    
    Only the status field can be updated.
    """
    try:
        service = OrderService(db)
        return service.update_order_status(order_id, order_update)
    except OrderNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An internal error occurred")

