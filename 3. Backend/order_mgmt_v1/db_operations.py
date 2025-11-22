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
            # created_at=datetime.now(timezone.utc)  # Set current timestamp
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
        
        # Return product data
        return {
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
 
        # Return order data with calculated totals
        return {
            "id": None,
            "user_id": None,
            "status": None,
            "created_at": None,
            "items": None,
            "total_amount_cents": None,
            "total_quantity": None
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


        # Convert ORM objects to dictionaries for easier handling
        # We need to iterate through each user object and extract its attributes
        users_list = []


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


        # Convert ORM objects to dictionaries for easier handling
        # We need to iterate through each product object and extract its attributes
        products_list = []
        
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
                    
        # Return orders list and total count
        return {
            "orders": None,
            "total": None
        }
    finally:
        # Always close the session
        db.close()

