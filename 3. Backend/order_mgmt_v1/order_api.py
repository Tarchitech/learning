"""
Order Management API

Simple Flask API that exposes database operations as REST endpoints.
This is a minimal implementation for learning purposes - no error handling.

Endpoints:
- POST /users - Create a new user
- POST /products - Create a new product
- POST /orders - Create a new order
- GET /users - List all users
- GET /products - List all products
- GET /orders?user_id=X - List orders for a specific user
"""

from flask import Flask, request, jsonify
from db_operations import (
    create_user,
    create_product,
    create_order,
    list_users,
    list_products,
    list_orders
)

# Create Flask application instance
app = Flask(__name__)


# ============================================================================
# LIST ENDPOINTS (GET)
# ============================================================================

@app.route('/users', methods=['GET'])
def api_list_users():
    """
    List all users in the database.
    
    Query parameters: None
    
    Returns: JSON object with list of users and total count
    {
        "users": [...],
        "total": 5
    }
    
    Example curl:
    curl -X GET http://localhost:8021/users
    """
    # Call database operation function (no parameters needed)
    
    
    # Return result as JSON response
    return "Empty list of users", 200


@app.route('/products', methods=['GET'])
def api_list_products():
    """
    List all products in the database.
    
    Query parameters: None
    
    Returns: JSON object with list of products and total count
    {
        "products": [...],
        "total": 10
    }
    
    Example curl:
    curl -X GET http://localhost:8021/products
    """
    # Call database operation function (no parameters needed)
    
    
    # Return result as JSON response
    return "Empty list of products", 200


@app.route('/orders', methods=['GET'])
def api_list_orders():
    """
    List all orders for a specific user.
    
    Query parameters:
    - user_id (required): The ID of the user whose orders to retrieve
    
    Example: GET /orders?user_id=1
    
    Returns: JSON object with list of orders and total count
    {
        "orders": [...],
        "total": 3
    }
    
    Example curl:
    curl -X GET "http://localhost:8021/orders?user_id=1"
    """
    # Get user_id from query parameters
    # request.args is a dictionary of query parameters
    
    
    # Call database operation function with user_id
    
    
    # Return result as JSON response
    return "Empty list of orders", 200


# ============================================================================
# CREATE ENDPOINTS (POST)
# ============================================================================

@app.route('/users', methods=['POST'])
def api_create_user():
    """
    Create a new user.
    
    Request body (JSON):
    {
        "email": "user@example.com",
        "full_name": "John Doe"
    }
    
    Returns: Created user data as JSON
    
    Example curl:
    curl -X POST http://localhost:8021/users \
      -H "Content-Type: application/json" \
      -d '{"email": "john@example.com", "full_name": "John Doe"}'
    """
    # Get JSON data from request body
    
    
    
    # Extract email and full_name from request data
    
    
    
    # Call database operation function
    
    
    # Return result as JSON response
    return "User created successfully", 201


@app.route('/products', methods=['POST'])
def api_create_product():
    """
    Create a new product.
    
    Request body (JSON):
    {
        "name": "MacBook Pro 16\"",
        "price_cents": 249999
    }
    
    Note: price_cents is price in cents (e.g., 249999 = $2499.99)
    
    Returns: Created product data as JSON
    
    Example curl:
    curl -X POST http://localhost:8021/products \
      -H "Content-Type: application/json" \
      -d '{"name": "MacBook Pro 16\\"", "price_cents": 249999}'
    """
    # Get JSON data from request body
    
    
    
    # Extract name and price_cents from request data
    

    # Call database operation function

    
    # Return result as JSON response
    return "Product created successfully", 201


@app.route('/orders', methods=['POST'])
def api_create_order():
    """
    Create a new order with items.
    
    Request body (JSON):
    {
        "user_id": 1,
        "status": "pending",
        "items": [
            {
                "product_id": 1,
                "quantity": 2
            },
            {
                "product_id": 2,
                "quantity": 1
            }
        ]
    }
    
    Returns: Created order data as JSON
    
    Example curl:
    curl -X POST http://localhost:8021/orders \
      -H "Content-Type: application/json" \
      -d '{"user_id": 1, "status": "pending", "items": [{"product_id": 1, "quantity": 2}, {"product_id": 2, "quantity": 1}]}'
    """
    # Get JSON data from request body
    
    
    
    # Extract order details from request data
    
    
    
    # Call database operation function
    
    
        
    # Return result as JSON response
    return "Order created successfully", 201



# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == '__main__':
    # Run the Flask development server
    # debug=True enables auto-reload on code changes (for development only)
    app.run(debug=True, host='0.0.0.0', port=8021)

