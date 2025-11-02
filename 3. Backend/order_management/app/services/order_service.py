"""
Order service for business logic operations.
"""
from typing import Optional, List, Tuple
from datetime import datetime
from sqlalchemy.orm import Session
from app.schemas.order import (
    OrderCreate, 
    OrderUpdate, 
    OrderResponse, 
    OrderListResponse, 
    OrderItemResponse,
    OrderStatusUpdateResponse
)
from app.repositories.order_repository import OrderRepository
from app.repositories.user_repository import UserRepository
from app.repositories.product_repository import ProductRepository
from app.utils.exceptions import (
    OrderNotFoundError,
    UserNotFoundError,
    ProductNotFoundError,
    ValidationError,
)
from app.core.security import validate_order_status
from app.utils.helpers import parse_iso_date


class OrderService:
    """Order service with business logic."""
    
    def __init__(self, db: Session):
        """
        Initialize order service.
        
        Args:
            db: Database session
        """
        self.repository = OrderRepository(db)
        self.user_repository = UserRepository(db)
        self.product_repository = ProductRepository(db)
        self.db = db
    
    def get_order(self, order_id: int) -> OrderResponse:
        """
        Get order by ID with items.
        
        Args:
            order_id: Order ID
            
        Returns:
            OrderResponse: Order response with items and totals
            
        Raises:
            OrderNotFoundError: If order not found
        """
        order = self.repository.get_with_items(order_id)
        if not order:
            raise OrderNotFoundError(f"Order with ID {order_id} not found")
        
        return self._order_to_response(order)
    
    def get_orders(
        self,
        status: Optional[str] = None,
        user_id: Optional[int] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        product_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 20,
    ) -> OrderListResponse:
        """
        Get orders with filters and aggregations.
        
        Args:
            status: Filter by order status
            user_id: Filter by user ID
            start_date: Filter orders from this date (ISO 8601)
            end_date: Filter orders until this date (ISO 8601)
            product_id: Filter orders containing this product
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            OrderListResponse: List of orders with aggregations
            
        Raises:
            ValidationError: If validation fails
        """
        # Validate status if provided
        if status and not validate_order_status(status):
            raise ValidationError(
                f"Invalid status. Must be one of: pending, paid, shipped, cancelled"
            )
        
        # Parse dates
        parsed_start_date = parse_iso_date(start_date) if start_date else None
        parsed_end_date = parse_iso_date(end_date) if end_date else None
        
        # Get orders with filters
        orders, total, total_amount_cents, total_quantity = (
            self.repository.get_all_with_filters(
                status=status,
                user_id=user_id,
                start_date=parsed_start_date,
                end_date=parsed_end_date,
                product_id=product_id,
                skip=skip,
                limit=limit,
            )
        )
        
        # Convert to response models
        # If product_id filter is applied, only include matching items in response
        order_responses = [
            self._order_to_response(order, product_id_filter=product_id)
            for order in orders
        ]
        
        return OrderListResponse(
            orders=order_responses,
            limit=limit,
            offset=skip,
            total_amount_cents=total_amount_cents,
            total_quantity=total_quantity,
        )
    
    def create_order(self, order_data: OrderCreate) -> OrderResponse:
        """
        Create a new order with items.
        
        Args:
            order_data: Order creation data
            
        Returns:
            OrderResponse: Created order
            
        Raises:
            UserNotFoundError: If user not found
            ProductNotFoundError: If product not found
            ValidationError: If validation fails
        """
        # Validate status
        if not validate_order_status(order_data.status):
            raise ValidationError(
                f"Invalid status. Must be one of: pending, paid, shipped, cancelled"
            )
        
        # Validate user exists
        user = self.user_repository.get(order_data.user_id)
        if not user:
            raise UserNotFoundError(f"User with ID {order_data.user_id} not found")
        
        # Validate products and get prices
        items_data = []
        for item in order_data.items:
            product = self.product_repository.get(item.product_id)
            if not product:
                raise ProductNotFoundError(
                    f"Product with ID {item.product_id} not found"
                )
            
            items_data.append({
                "product_id": item.product_id,
                "quantity": item.quantity,
                "price_cents_at_purchase": product.price_cents,
            })
        
        # Create order with items
        order = self.repository.create_with_items(
            order_data={
                "user_id": order_data.user_id,
                "status": order_data.status,
            },
            items_data=items_data,
        )
        
        return self._order_to_response(order)
    
    def update_order_status(
        self,
        order_id: int,
        order_update: OrderUpdate,
    ) -> OrderStatusUpdateResponse:
        """
        Update order status.
        
        Args:
            order_id: Order ID
            order_update: Order update data (status)
            
        Returns:
            OrderResponse: Updated order
            
        Raises:
            OrderNotFoundError: If order not found
            ValidationError: If validation fails
        """
        # Validate status
        if not validate_order_status(order_update.status):
            raise ValidationError(
                f"Invalid status. Must be one of: pending, paid, shipped, cancelled"
            )
        
        # Update order
        order = self.repository.update_status(order_id, order_update.status)
        if not order:
            raise OrderNotFoundError(f"Order with ID {order_id} not found")
        
        # Reload to get updated_at
        order = self.repository.get(order_id)
        if not order:
            raise OrderNotFoundError(f"Order with ID {order_id} not found")
        
        return OrderStatusUpdateResponse(
            order_id=order.id,
            user_id=order.user_id,
            status=order.status,
            created_at=order.created_at,
            updated_at=order.updated_at,
        )
    
    def _order_to_response(
        self, 
        order, 
        product_id_filter: Optional[int] = None
    ) -> OrderResponse:
        """
        Convert order model to response schema.
        
        Args:
            order: Order model instance
            product_id_filter: Optional product ID to filter items (only include matching items)
            
        Returns:
            OrderResponse: Order response with calculated totals
        """
        # Filter items if product_id filter is provided
        if product_id_filter is not None:
            filtered_items = [
                item for item in order.items 
                if item.product_id == product_id_filter
            ]
        else:
            filtered_items = order.items
        
        # Calculate totals for this order (only for filtered items)
        total_amount_cents = sum(
            item.quantity * item.price_cents_at_purchase for item in filtered_items
        )
        total_quantity = sum(item.quantity for item in filtered_items)
        
        # Build order items with product names
        order_items = []
        for item in filtered_items:
            item_dict = {
                "id": item.id,
                "product_id": item.product_id,
                "quantity": item.quantity,
                "price_cents_at_purchase": item.price_cents_at_purchase,
                "product_name": item.product.name if item.product else None
            }
            order_items.append(OrderItemResponse(**item_dict))
        
        # Get user name from relationship
        user_name = order.user.full_name if order.user else None
        
        # Create response with order_id instead of id
        response_dict = {
            "order_id": order.id,
            "user_id": order.user_id,
            "status": order.status,
            "created_at": order.created_at,
            "items": order_items,
            "total_amount_cents": total_amount_cents,
            "total_quantity": total_quantity,
            "user_name": user_name,
        }
        return OrderResponse(**response_dict)

