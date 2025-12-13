"""
Database Operations Module

This module contains the core database operation functions:
1. create_user - Create a new user
2. create_product - Create a new product
3. create_order - Create a new order with items
4. list_orders - List all orders for a specific user

These functions handle all database interactions using SQLAlchemy ORM.
"""
from datetime import datetime, timezone
from sqlalchemy.orm import joinedload
from database import get_db
# Import models - using the generated model names (Users, Products, Orders, OrderItems)
from models import Users, Products, Orders, OrderItems


def create_user(email: str, full_name: str) -> dict:
    """
    Create a new user in the database.
    
    This function creates a new user record with the provided email and full name.
    The database will automatically assign an ID and creation timestamp.
    
    Args:
        email: User's email address (must be unique)
        full_name: User's full name
    
    Returns:
        Dictionary containing the created user's data:
        {
            "id": int,
            "email": str,
            "full_name": str,
            "created_at": str (ISO format)
        }
    """
    # Create a new database session
    # Each function call gets its own session to ensure data consistency
    db = get_db()
    
    try:
        # Create a new Users object with the provided data
        # The ORM will map this to a row in the users table
        new_user = Users(
            email=email,
            full_name=full_name,
            created_at=datetime.now(timezone.utc)  # Set current timestamp
        )
        
        # Add the user to the session (stages it for insertion)
        db.add(new_user)
        
        # Commit the transaction (actually saves to database)
        db.commit()
        
        # Refresh to get database-generated values (like auto-incremented ID)
        db.refresh(new_user)
        
        # Return user data as a dictionary
        return {
            "id": new_user.id,
            "email": new_user.email,
            "full_name": new_user.full_name,
            "created_at": new_user.created_at.isoformat() if new_user.created_at else None
        }
    finally:
        # Always close the session, even if an error occurs
        db.close()


def create_product(name: str, price_cents: int) -> dict:
    """
    Create a new product in the database.
    
    This function creates a new product record with the provided name and price.
    Price is stored in cents to avoid floating-point precision issues.
    
    Args:
        name: Product name (e.g., "MacBook Pro 16\"")
        price_cents: Price in cents (e.g., 249999 = $2499.99)
    
    Returns:
        Dictionary containing the created product's data:
        {
            "id": int,
            "name": str,
            "price_cents": int
        }
    """
    # Create a new database session
    db = get_db()
    
    try:
        # Create a new Products object
        new_product = Products(
            name=name,
            price_cents=price_cents
        )
        
        # Add to session and commit
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        
        # Return product data
        return {
            "id": new_product.id,
            "name": new_product.name,
            "price_cents": new_product.price_cents
        }
    finally:
        # Always close the session
        db.close()


def create_order(user_id: int, status: str, items: list) -> dict:
    """
    Create a new order with multiple items.
    
    This function creates an order and all its line items in a single transaction.
    It captures the product price at purchase time, so if prices change later,
    the order still reflects what the customer actually paid.
    
    Args:
        user_id: ID of the user placing the order
        status: Order status (e.g., "pending", "paid", "shipped", "cancelled")
        items: List of dictionaries, each containing:
            {
                "product_id": int,
                "quantity": int
            }
    
    Returns:
        Dictionary containing the created order's data:
        {
            "id": int,
            "user_id": int,
            "status": str,
            "created_at": str (ISO format),
            "items": list of item dictionaries,
            "total_amount_cents": int,
            "total_quantity": int
        }
    """
    # Create a new database session
    db = get_db()
    
    try:
        # Step 1: Create the order record
        # We use flush() to get the order ID without committing yet
        # This allows us to link order items to the order before committing
        new_order = Orders(
            user_id=user_id,
            status=status,
            created_at=datetime.now(timezone.utc)
        )
        db.add(new_order)
        db.flush()  # Gets the order ID from database without committing
        
        # Step 2: Initialize variables to track totals
        total_amount = 0  # Total price in cents for all items
        total_quantity = 0  # Total number of items
        items_list = []  # List to store item data for response
        
        # Step 3: Create order items for each product in the order
        for item_data in items:
            # Fetch the product to get its current price
            # This ensures we capture the price at the time of purchase
            product = db.query(Products).filter(Products.id == item_data["product_id"]).first()
            
            # Calculate total price for this line item (unit price * quantity)
            price_at_purchase = product.price_cents * item_data["quantity"]
            
            # Create the order item record
            # We store price_at_purchase so we remember what was charged
            # even if product price changes later
            order_item = OrderItems(
                order_id=new_order.id,  # Link to the order we just created
                product_id=item_data["product_id"],
                quantity=item_data["quantity"],
                price_cents_at_purchase=price_at_purchase
            )
            db.add(order_item)
            
            # Update running totals
            total_amount += price_at_purchase
            total_quantity += item_data["quantity"]
            
            # Store item data for response (ID will be added after commit)
            items_list.append({
                "product_id": order_item.product_id,
                "quantity": order_item.quantity,
                "price_cents_at_purchase": order_item.price_cents_at_purchase,
                "product_name": product.name if product else None
            })
        
        # Step 4: Commit all changes to database (order + all items in one transaction)
        # This ensures atomicity - either all items are saved or none are
        db.commit()
        
        # Reload order with items to get all database-assigned IDs
        db.refresh(new_order)
        new_order = db.query(Orders).filter(Orders.id == new_order.id).first()
        
        # Add IDs to items_list after they've been assigned by database
        # Note: Generated model uses 'order_items' relationship name
        for i, db_item in enumerate(new_order.order_items):
            items_list[i]["id"] = db_item.id
        
        # Return order data with calculated totals
        return {
            "id": new_order.id,
            "user_id": new_order.user_id,
            "status": new_order.status,
            "created_at": new_order.created_at.isoformat() if new_order.created_at else None,
            "items": items_list,
            "total_amount_cents": total_amount,
            "total_quantity": total_quantity
        }
    finally:
        # Always close the session
        db.close()

def list_users() -> dict:
    """
    List all users in the database.
    
    This function retrieves all users from the database and returns them
    in a dictionary format. It's useful for displaying all registered users
    or checking what users exist in the system.
    
    Returns:
        Dictionary containing:
        {
            "users": list of user dictionaries,
            "total": int (count of users)
        }
        
        Each user dictionary contains:
        {
            "id": int,
            "email": str,
            "full_name": str,
            "created_at": str (ISO format) or None
        }
    """
    # Create a new database session
    # Each function call gets its own session to ensure data consistency
    db = get_db()
    
    try:
        # Query all users from the database
        # db.query(Users): Start a query targeting the Users model/table
        # .all(): Execute the query and return all matching records as a list
        # This will return a list of Users ORM objects
        users = db.query(Users).all()
        
        # Convert ORM objects to dictionaries for easier handling
        # We need to iterate through each user object and extract its attributes
        users_list = []
        for user in users:
            # For each user object, create a dictionary with its data
            # This makes it easier to work with the data (e.g., for JSON serialization)
            user_dict = {
                "id": user.id,  # Get the user's ID (primary key)
                "email": user.email,  # Get the user's email address
                "full_name": user.full_name,  # Get the user's full name
                # Convert created_at to ISO format string if it exists, otherwise None
                # ISO format is a standard date/time format (e.g., "2024-01-15T10:30:00")
                "created_at": user.created_at.isoformat() if user.created_at else None
            }
            users_list.append(user_dict)
        
        # Return the result as a dictionary
        # This format is consistent with other list functions in this module
        return {
            "users": users_list,  # List of user dictionaries
            "total": len(users_list)  # Total count of users
        }
    finally:
        # Always close the session, even if an error occurs
        # This ensures database connections are properly released
        # If we don't close the session, we could run out of database connections
        db.close()

def list_products() -> dict:
    """
    List all products in the database.
    
    This function retrieves all products from the database and returns them
    in a dictionary format. It's useful for displaying the product catalog
    or checking what products are available in the system.
    
    Returns:
        Dictionary containing:
        {
            "products": list of product dictionaries,
            "total": int (count of products)
        }
        
        Each product dictionary contains:
        {
            "id": int,
            "name": str,
            "price_cents": int (price in cents, e.g., 2499 = $24.99)
        }
    """
    # Create a new database session
    # Each function call gets its own session to ensure data consistency
    db = get_db()
    
    try:
        # Query all products from the database
        # db.query(Products): Start a query targeting the Products model/table
        # .all(): Execute the query and return all matching records as a list
        # This will return a list of Products ORM objects
        products = db.query(Products).all()
        
        # Convert ORM objects to dictionaries for easier handling
        # We need to iterate through each product object and extract its attributes
        products_list = []
        for product in products:
            # For each product object, create a dictionary with its data
            # This makes it easier to work with the data (e.g., for JSON serialization)
            product_dict = {
                "id": product.id,  # Get the product's ID (primary key)
                "name": product.name,  # Get the product's name
                # Get the product's price in cents
                # Note: Price is stored in cents to avoid floating-point precision issues
                # For example, 249999 cents = $2499.99
                "price_cents": product.price_cents
            }
            products_list.append(product_dict)
        
        # Return the result as a dictionary
        # This format is consistent with other list functions in this module
        return {
            "products": products_list,  # List of product dictionaries
            "total": len(products_list)  # Total count of products
        }
    finally:
        # Always close the session, even if an error occurs
        # This ensures database connections are properly released
        # If we don't close the session, we could run out of database connections
        db.close()

def list_orders(user_id: int) -> dict:
    """
    List all orders for a specific user.
    
    This function retrieves all orders belonging to the specified user.
    It includes order details, all items in each order, and calculated totals.
    Also includes user name and product names for convenience.
    
    Args:
        user_id: The ID of the user whose orders to retrieve
    
    Returns:
        Dictionary containing:
        {
            "orders": list of order dictionaries,
            "total": int (count of orders)
        }
        
        Each order dictionary contains:
        {
            "id": int,
            "user_id": int,
            "user_name": str,
            "status": str,
            "created_at": str (ISO format),
            "items": list of item dictionaries,
            "total_amount_cents": int,
            "total_quantity": int
        }
    """
    # Create a new database session
    db = get_db()
    
    try:
        # Query orders for the user with relationships pre-loaded
        # joinedload(Orders.user): Load user data in the same query (for user_name)
        # joinedload(Orders.order_items).joinedload(OrderItems.product): Load all items and their products
        # Note: Generated model uses 'order_items' relationship name instead of 'items'
        # This prevents multiple database queries (N+1 problem)
        orders = db.query(Orders).options(
            joinedload(Orders.user),  # Eagerly load user relationship
            joinedload(Orders.order_items).joinedload(OrderItems.product)  # Eagerly load items and products
        ).filter(Orders.user_id == user_id).all()
        
        # Using Lazy Loading (not recommended, will have performance issues)
        # orders = db.query(Orders).filter(Orders.user_id == user_id).all()

        # Then accessing relationships will trigger additional queries
        # for order in orders:
        #     # This will trigger a query
        #     user_name = order.user.full_name
        #     for item in order.order_items:
        #         product_name = item.product.name

        # Build response list
        orders_list = []
        for order in orders:
            # Calculate totals for this order by summing up all items
            # Note: Generated model uses 'order_items' relationship name
            total_amount = sum(item.price_cents_at_purchase for item in order.order_items)
            total_quantity = sum(item.quantity for item in order.order_items)
            
            # Build list of order items with product names
            items = [
                {
                    "id": item.id,
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "price_cents_at_purchase": item.price_cents_at_purchase,
                    "product_name": item.product.name if item.product else None
                }
                for item in order.order_items
            ]
            
            # Add order data to response list
            orders_list.append({
                "id": order.id,
                "user_id": order.user_id,
                "user_name": order.user.full_name if order.user else None,
                "status": order.status,
                "created_at": order.created_at.isoformat() if order.created_at else None,
                "items": items,
                "total_amount_cents": total_amount,
                "total_quantity": total_quantity
            })
        
        # Return orders list and total count
        return {
            "orders": orders_list,
            "total": len(orders_list)
        }
    finally:
        # Always close the session
        db.close()

