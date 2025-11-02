"""
Order repository for data access operations.
"""
from typing import Optional, List, Tuple
from datetime import datetime
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, and_, or_
from app.models.order import Order
from app.models.order_item import OrderItem
from app.repositories.base import BaseRepository


class OrderRepository(BaseRepository[Order]):
    """Order repository with order-specific operations."""
    
    def __init__(self, db: Session):
        """Initialize order repository."""
        super().__init__(Order, db)
    
    def get_with_items(self, id: int) -> Optional[Order]:
        """
        Get order with items using eager loading.
        
        Args:
            id: Order ID
            
        Returns:
            Optional[Order]: Order with items or None if not found
        """
        from app.models.product import Product
        from app.models.user import User
        
        return (
            self.db.query(Order)
            .options(
                joinedload(Order.items).joinedload(OrderItem.product),
                joinedload(Order.user)
            )
            .filter(Order.id == id)
            .first()
        )
    
    def get_all_with_filters(
        self,
        status: Optional[str] = None,
        user_id: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        product_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 20,
    ) -> Tuple[List[Order], int, int, int]:
        """
        Get orders with filters and aggregations.
        
        Args:
            status: Filter by order status
            user_id: Filter by user ID
            start_date: Filter orders from this date
            end_date: Filter orders until this date
            product_id: Filter orders containing this product
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            Tuple: (list of orders, total count, total_amount_cents, total_quantity)
        """
        from app.models.product import Product
        from app.models.user import User
        
        query = self.db.query(Order).options(
            joinedload(Order.items).joinedload(OrderItem.product),
            joinedload(Order.user)
        )
        
        # Apply filters
        if status:
            query = query.filter(Order.status == status)
        if user_id:
            query = query.filter(Order.user_id == user_id)
        if start_date:
            query = query.filter(Order.created_at >= start_date)
        if end_date:
            query = query.filter(Order.created_at <= end_date)
        if product_id:
            # Filter orders that have items with this product_id
            query = query.join(OrderItem).filter(OrderItem.product_id == product_id)
        
        # Get total count
        total = query.count()
        
        # Get paginated results
        orders = query.offset(skip).limit(limit).all()
        
        # Calculate aggregations across all filtered results (not just current page)
        aggregation_query = (
            self.db.query(
                func.sum(OrderItem.quantity * OrderItem.price_cents_at_purchase).label("total_amount"),
                func.sum(OrderItem.quantity).label("total_qty")
            )
            .join(Order, OrderItem.order_id == Order.id)
        )
        
        # Apply same filters to aggregation
        if status:
            aggregation_query = aggregation_query.filter(Order.status == status)
        if user_id:
            aggregation_query = aggregation_query.filter(Order.user_id == user_id)
        if start_date:
            aggregation_query = aggregation_query.filter(Order.created_at >= start_date)
        if end_date:
            aggregation_query = aggregation_query.filter(Order.created_at <= end_date)
        if product_id:
            aggregation_query = aggregation_query.filter(OrderItem.product_id == product_id)
        
        result = aggregation_query.first()
        total_amount_cents = int(result.total_amount or 0)
        total_quantity = int(result.total_qty or 0)
        
        return orders, total, total_amount_cents, total_quantity
    
    def create_with_items(self, order_data: dict, items_data: List[dict]) -> Order:
        """
        Create order with items in a transaction.
        
        Args:
            order_data: Order data dictionary
            items_data: List of order item data dictionaries
            
        Returns:
            Order: Created order with items
        """
        # Create order
        order = Order(**order_data)
        self.db.add(order)
        self.db.flush()  # Flush to get order ID
        
        # Create order items
        for item_data in items_data:
            item_data["order_id"] = order.id
            order_item = OrderItem(**item_data)
            self.db.add(order_item)
        
        self.db.commit()
        self.db.refresh(order)
        
        # Reload with items
        return self.get_with_items(order.id)
    
    def update_status(self, id: int, status: str) -> Optional[Order]:
        """
        Update order status.
        
        Args:
            id: Order ID
            status: New status
            
        Returns:
            Optional[Order]: Updated order or None if not found
        """
        from datetime import datetime
        return self.update(id, {"status": status, "updated_at": datetime.utcnow()})

