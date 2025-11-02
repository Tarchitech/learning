# Order Management System - Product Requirements Document

## 1. Project Overview

### 1.1 Project Goal
Create a comprehensive order management system backend API that provides searching, creating, and updating functionality for orders, products, and users. The system should support multi-dimensional filtering, aggregation, and maintain data integrity through proper relationships.

### 1.2 Technology Stack
- **Framework**: FastAPI (modern, fast, async Python web framework)
- **ORM**: SQLAlchemy (for database operations and entity definitions)
- **Validation**: Pydantic (for request/response schema validation)
- **Database**: PostgreSQL (via Neon.tech)
- **Testing**: pytest (with pytest-asyncio for async tests)
- **API Documentation**: FastAPI auto-generated OpenAPI/Swagger docs

### 1.3 Database Architecture
The system uses a PostgreSQL database with the following schema:

- **Schema**: `tony`
- **Tables**:
  - `users`: User information (id, email, full_name, created_at)
  - `orders`: Order headers (id, user_id, status, created_at)
  - `products`: Product catalog (id, name, price_cents)
  - `order_items`: Order line items (id, order_id, product_id, quantity, price_cents_at_purchase)

**Relationships**:
- `orders.user_id` → `users.id` (Foreign Key)
- `order_items.order_id` → `orders.id` (Foreign Key)
- `order_items.product_id` → `products.id` (Foreign Key)

**Constraints**:
- Order status: `pending`, `paid`, `shipped`, `cancelled`
- Product price must be >= 0
- Order item quantity must be > 0
- User email must be unique

## 2. API Specification

### 2.1 RESTful API Design Principles
- Use standard HTTP methods (GET, POST, PUT, PATCH)
- Resource-based URLs (e.g., `/api/v1/orders`, `/api/v1/products`)
- Consistent response formats
- Proper HTTP status codes
- Version API endpoints (`/api/v1/`)

### 2.2 API Endpoints

#### 2.2.1 Orders API

##### GET `/api/v1/orders`
List all orders with optional filtering.

**Query Parameters**:
- `status` (optional): Filter by order status (`pending`, `paid`, `shipped`, `cancelled`)
- `user_id` (optional): Filter by user ID
- `start_date` (optional): Filter orders from this date (ISO 8601 format, e.g., `2024-01-01T00:00:00Z`)
- `end_date` (optional): Filter orders until this date (ISO 8601 format)
- `product_id` (optional): Filter orders containing this product ID
- `limit` (optional): Number of results per page (default: 20, max: 100)
- `offset` (optional): Number of results to skip (default: 0)

**Response**:
```json
{
  "items": [
    {
      "id": 1,
      "user_id": 1,
      "status": "paid",
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
  ],
  "total": 150,
  "limit": 20,
  "offset": 0,
  "total_amount_cents": 500000,
  "total_quantity": 250
}
```

**Status Codes**:
- `200 OK`: Success
- `400 Bad Request`: Invalid query parameters
- `500 Internal Server Error`: Server error

##### POST `/api/v1/orders`
Create a new order.

**Request Body**:
```json
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
```

**Validation Rules**:
- `user_id`: Required, must exist in users table
- `status`: Required, must be one of: `pending`, `paid`, `shipped`, `cancelled`
- `items`: Required, must be a non-empty array
- Each item:
  - `product_id`: Required, must exist in products table
  - `quantity`: Required, must be > 0

**Response**:
```json
{
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
```

**Status Codes**:
- `201 Created`: Order created successfully
- `400 Bad Request`: Validation error or invalid data
- `404 Not Found`: User or product not found
- `500 Internal Server Error`: Server error

##### PATCH `/api/v1/orders/{order_id}`
Update an order's status.

**Path Parameters**:
- `order_id`: Order ID (integer)

**Request Body**:
```json
{
  "status": "paid"
}
```

**Validation Rules**:
- `status`: Required, must be one of: `pending`, `paid`, `shipped`, `cancelled`

**Response**:
```json
{
  "id": 1,
  "user_id": 1,
  "status": "paid",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T11:00:00Z"
}
```

**Status Codes**:
- `200 OK`: Order updated successfully
- `400 Bad Request`: Invalid status value
- `404 Not Found`: Order not found
- `500 Internal Server Error`: Server error

#### 2.2.2 Products API

##### GET `/api/v1/products`
List all products.

**Query Parameters**:
- `limit` (optional): Number of results per page (default: 20, max: 100)
- `offset` (optional): Number of results to skip (default: 0)

**Response**:
```json
{
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
```

**Status Codes**:
- `200 OK`: Success
- `500 Internal Server Error`: Server error

##### POST `/api/v1/products`
Create a new product.

**Request Body**:
```json
{
  "name": "Product A",
  "price_cents": 1999
}
```

**Validation Rules**:
- `name`: Required, non-empty string, max 255 characters
- `price_cents`: Required, integer >= 0

**Response**:
```json
{
  "id": 1,
  "name": "Product A",
  "price_cents": 1999
}
```

**Status Codes**:
- `201 Created`: Product created successfully
- `400 Bad Request`: Validation error
- `500 Internal Server Error`: Server error

##### PATCH `/api/v1/products/{product_id}`
Update a product's name and/or price.

**Path Parameters**:
- `product_id`: Product ID (integer)

**Request Body**:
```json
{
  "name": "Updated Product A",
  "price_cents": 2499
}
```

**Validation Rules**:
- `name`: Optional, non-empty string if provided, max 255 characters
- `price_cents`: Optional, integer >= 0 if provided
- At least one field must be provided

**Response**:
```json
{
  "id": 1,
  "name": "Updated Product A",
  "price_cents": 2499
}
```

**Status Codes**:
- `200 OK`: Product updated successfully
- `400 Bad Request`: Validation error
- `404 Not Found`: Product not found
- `500 Internal Server Error`: Server error

#### 2.2.3 Users API

##### GET `/api/v1/users`
List all users.

**Query Parameters**:
- `limit` (optional): Number of results per page (default: 20, max: 100)
- `offset` (optional): Number of results to skip (default: 0)

**Response**:
```json
{
  "items": [
    {
      "id": 1,
      "email": "user@example.com",
      "full_name": "John Doe",
      "created_at": "2024-01-10T08:00:00Z"
    }
  ],
  "total": 100,
  "limit": 20,
  "offset": 0
}
```

**Status Codes**:
- `200 OK`: Success
- `500 Internal Server Error`: Server error

##### PATCH `/api/v1/users/{user_id}`
Update a user's information (email and/or full name).

**Path Parameters**:
- `user_id`: User ID (integer)

**Request Body**:
```json
{
  "email": "newemail@example.com",
  "full_name": "Jane Doe"
}
```

**Validation Rules**:
- `email`: Optional, valid email format if provided, must be unique
- `full_name`: Optional, non-empty string if provided, max 255 characters
- At least one field must be provided

**Response**:
```json
{
  "id": 1,
  "email": "newemail@example.com",
  "full_name": "Jane Doe",
  "created_at": "2024-01-10T08:00:00Z"
}
```

**Status Codes**:
- `200 OK`: User updated successfully
- `400 Bad Request`: Validation error (e.g., invalid email format, duplicate email)
- `404 Not Found`: User not found
- `409 Conflict`: Email already exists
- `500 Internal Server Error`: Server error

### 2.3 Error Response Format
All errors should follow this format:

```json
{
  "detail": "Error message describing what went wrong",
  "code": "ERROR_CODE",
  "field": "field_name" // Optional, for field-specific errors
}
```

### 2.4 Aggregation Requirements
As per additional requirements:
- When listing orders that contain quantity information, include `total_quantity` in the response
- When listing orders that contain amount information, include `total_amount_cents` in the response
- These aggregations should be calculated across all filtered results, not just the current page

## 3. Project Structure

### 3.1 Folder Structure
Following a layered architecture pattern for maintainability and testability:

```
order_management/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application entry point
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── orders.py          # Order-related endpoints
│   │   │   ├── products.py        # Product-related endpoints
│   │   │   └── users.py           # User-related endpoints
│   │   └── deps.py                # API dependencies (e.g., DB session)
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py              # Configuration management (env vars)
│   │   ├── database.py            # Database connection and session
│   │   └── security.py            # Security utilities (validation, encryption)
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py                # Base model class with common fields
│   │   ├── user.py                # User ORM model
│   │   ├── order.py               # Order ORM model
│   │   ├── product.py             # Product ORM model
│   │   └── order_item.py          # OrderItem ORM model
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── order.py               # Order Pydantic schemas (request/response)
│   │   ├── product.py             # Product Pydantic schemas
│   │   └── user.py                # User Pydantic schemas
│   ├── services/
│   │   ├── __init__.py
│   │   ├── order_service.py       # Order business logic
│   │   ├── product_service.py     # Product business logic
│   │   └── user_service.py        # User business logic
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── base.py                # Base repository with common CRUD operations
│   │   ├── order_repository.py    # Order data access layer
│   │   ├── product_repository.py  # Product data access layer
│   │   └── user_repository.py     # User data access layer
│   └── utils/
│       ├── __init__.py
│       ├── exceptions.py          # Custom exception classes
│       └── helpers.py             # Helper functions (e.g., date parsing)
├── tests/
│   ├── __init__.py
│   ├── conftest.py                # pytest configuration and fixtures
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_services/
│   │   │   ├── __init__.py
│   │   │   ├── test_order_service.py
│   │   │   ├── test_product_service.py
│   │   │   └── test_user_service.py
│   │   ├── test_repositories/
│   │   │   ├── __init__.py
│   │   │   ├── test_order_repository.py
│   │   │   ├── test_product_repository.py
│   │   │   └── test_user_repository.py
│   │   └── test_utils/
│   │       ├── __init__.py
│   │       └── test_helpers.py
│   ├── integration/
│   │   ├── __init__.py
│   │   └── test_api/
│   │       ├── __init__.py
│   │       ├── test_orders_api.py
│   │       ├── test_products_api.py
│   │       └── test_users_api.py
│   └── fixtures/
│       ├── __init__.py
│       └── sample_data.py         # Test data fixtures
├── .env.example                   # Environment variables template
├── .env                           # Environment variables (not in git)
├── .gitignore                     # Git ignore rules
├── requirements.txt               # Python dependencies
├── requirements-dev.txt           # Development dependencies (pytest, etc.)
├── pytest.ini                     # pytest configuration
├── README.md                      # Project documentation
└── postman_collection.json        # Postman collection for API testing
```

### 3.2 Architecture Layers

1. **API Layer** (`app/api/`): Handles HTTP requests/responses, input validation, routing
2. **Service Layer** (`app/services/`): Contains business logic, orchestration
3. **Repository Layer** (`app/repositories/`): Data access abstraction, database operations
4. **Model Layer** (`app/models/`): SQLAlchemy ORM models representing database entities
5. **Schema Layer** (`app/schemas/`): Pydantic models for request/response validation and serialization

## 4. Security Best Practices

### 4.1 Input Validation and Sanitization
- Use Pydantic schemas for all request validation
- Validate data types, ranges, and formats (e.g., email validation)
- Sanitize string inputs to prevent injection attacks
- Reject requests with unexpected fields

### 4.2 SQL Injection Prevention
- Use SQLAlchemy ORM exclusively - never use raw SQL queries with string interpolation
- Use parameterized queries if raw SQL is absolutely necessary (not recommended)
- Validate all user inputs before database operations

### 4.3 Environment Variables
- Store sensitive information (database credentials, API keys) in environment variables
- Use `.env` file for local development (not committed to git)
- Provide `.env.example` with placeholder values
- Never hardcode credentials in source code
- Use `python-dotenv` to load environment variables

### 4.4 API Security Considerations
- Implement CORS middleware with appropriate allowed origins
- Consider rate limiting for production (optional for MVP)
- Use HTTPS in production
- Implement proper error handling that doesn't leak sensitive information

### 4.5 Data Validation
- Use Pydantic for request/response validation
- Validate foreign key relationships (user_id, product_id exist)
- Enforce business rules (quantity > 0, price >= 0, unique email)
- Validate enum values (order status)

### 4.6 Logging
- Log all API requests with appropriate log levels
- Never log sensitive information (passwords, tokens, full request bodies)
- Include request IDs for traceability
- Log errors with sufficient context for debugging

## 5. Coding Standards

### 5.1 Python Code Style
- Follow PEP 8 style guide
- Use black or similar formatter for consistent formatting
- Maximum line length: 88 characters (black default)
- Use 4 spaces for indentation (no tabs)

### 5.2 Type Hints
- Use type hints for all function parameters and return types
- Use `typing` module for complex types (List, Dict, Optional, Union)
- Example:
```python
from typing import List, Optional
from app.schemas.order import OrderCreate, OrderResponse

def create_order(order_data: OrderCreate, db: Session) -> OrderResponse:
    ...
```

### 5.3 Docstrings
- Use Google-style docstrings for all public functions and classes
- Include parameter descriptions, return type, and possible exceptions
- Example:
```python
def get_orders(
    status: Optional[str] = None,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db)
) -> List[OrderResponse]:
    """
    Retrieve orders with optional filtering.

    Args:
        status: Optional order status filter (pending, paid, shipped, cancelled)
        user_id: Optional user ID filter
        db: Database session dependency

    Returns:
        List of OrderResponse objects

    Raises:
        ValueError: If status value is invalid
    """
```

### 5.4 Error Handling
- Use custom exception classes for different error types
- Return appropriate HTTP status codes
- Provide clear, user-friendly error messages
- Log errors with context for debugging
- Example exception structure:
```python
class OrderNotFoundError(Exception):
    """Raised when an order is not found."""
    pass

class ValidationError(Exception):
    """Raised when input validation fails."""
    pass
```

### 5.5 Dependency Injection
- Use FastAPI's dependency injection system
- Create reusable dependencies (e.g., database session)
- Keep business logic in services, not in API endpoints

### 5.6 Language Requirement
- **All code, comments, and documentation must be in English**
- Variable names, function names, class names must be in English
- Docstrings and inline comments must be in English
- Error messages and log messages must be in English
- Documentation files (README, PRD, etc.) must be in English

## 6. Database Configuration

### 6.1 Environment Variables
Create a `.env` file (not committed to git) with the following variables:

```env
# Database Configuration
DB_HOST=ep-jolly-feather-adyuujqy-pooler.c-2.us-east-1.aws.neon.tech
DB_PORT=5432
DB_NAME=neondb
DB_USER=<username>
DB_PASSWORD=<password>
DB_SCHEMA=tony

# Application Configuration
API_V1_PREFIX=/api/v1
DEBUG=False
LOG_LEVEL=INFO
```

### 6.2 Configuration Management
- Use `pydantic-settings` or `python-dotenv` for configuration
- Create a `Config` class in `app/core/config.py` that reads from environment variables
- Provide sensible defaults where appropriate
- Validate configuration on application startup

### 6.3 SQLAlchemy Configuration
- Use SQLAlchemy connection pooling
- Configure connection pool size appropriately
- Use connection string format:
  `postgresql://{user}:{password}@{host}:{port}/{database}`
- Set schema search path if needed

### 6.4 Database Migration (Optional)
- Consider using Alembic for database migrations in future
- For initial setup, database schema is already created via SQL script

## 7. Testing Strategy

### 7.1 Testing Framework
- Use `pytest` as the testing framework
- Use `pytest-asyncio` for async test support
- Use `pytest-cov` for coverage reporting

### 7.2 Test Structure
- **Unit Tests**: Test individual functions and methods in isolation
  - Service layer tests (mock repositories)
  - Repository layer tests (mock database)
  - Utility function tests
  
- **Integration Tests**: Test API endpoints with test database
  - Use test database (separate from development/production)
  - Test full request/response cycle
  - Test error scenarios

### 7.3 Test Coverage Targets
- Aim for minimum 80% code coverage
- Focus on business logic and critical paths
- Test edge cases and error conditions

### 7.4 Test Fixtures
- Use pytest fixtures for common setup (database session, test data)
- Create reusable fixtures in `conftest.py`
- Use factories for creating test data

### 7.5 Mocking
- Mock external dependencies (database, external APIs)
- Use `unittest.mock` or `pytest-mock` for mocking
- Mock repository layer in service tests
- Use test database in integration tests

### 7.6 Example Test Structure
```python
# tests/unit/test_services/test_order_service.py
import pytest
from unittest.mock import Mock, patch
from app.services.order_service import OrderService
from app.schemas.order import OrderCreate

def test_create_order_success(mock_db, sample_order_data):
    """Test successful order creation."""
    service = OrderService()
    result = service.create_order(sample_order_data, mock_db)
    assert result.id is not None
    assert result.status == "pending"

def test_create_order_invalid_user(mock_db, sample_order_data):
    """Test order creation with invalid user ID."""
    service = OrderService()
    with pytest.raises(ValueError):
        service.create_order(sample_order_data, mock_db)
```

## 8. Development Tools and Documentation

### 8.1 API Documentation - Swagger/OpenAPI
FastAPI automatically generates OpenAPI/Swagger documentation. The following requirements must be met:

**Documentation Endpoints**:
- `/docs` - Swagger UI (interactive API documentation)
- `/redoc` - ReDoc (alternative documentation UI)
- `/openapi.json` - OpenAPI JSON schema (for API clients)

**Required Documentation Elements for Each Endpoint**:
- **Summary**: Brief one-line description (shown in endpoint list)
- **Description**: Detailed description explaining the endpoint's purpose
- **Tags**: Organizational tags for grouping endpoints (e.g., "orders", "products", "users")
- **Response Models**: Proper Pydantic models for all response types
- **Response Codes**: Documentation for all possible HTTP status codes (200, 201, 400, 404, 409, 500)
- **Query Parameters**: Descriptions, types, examples, and validation rules
- **Path Parameters**: Descriptions and examples
- **Request Body Examples**: Pre-filled example requests in Swagger UI
- **Response Examples**: Example responses for success and error cases
- **Error Responses**: Detailed error response schemas with examples

**FastAPI Application Configuration**:
Configure the FastAPI app with comprehensive metadata:

```python
app = FastAPI(
    title="Order Management System API",
    description="Comprehensive REST API for managing orders, products, and users with full CRUD operations",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    tags_metadata=[
        {
            "name": "orders",
            "description": "Operations related to order management. Supports listing with multi-dimensional filtering, creation, and status updates.",
        },
        {
            "name": "products",
            "description": "Operations related to product catalog management. Create, list, and update products.",
        },
        {
            "name": "users",
            "description": "Operations related to user management. List and update user information.",
        },
    ],
)
```

**Endpoint Documentation Example**:
```python
@router.get(
    "/orders",
    summary="List orders",
    description="Retrieve a list of orders with optional filtering by status, user, date range, or product. Returns paginated results with aggregation totals.",
    tags=["orders"],
    response_model=OrderListResponse,
    responses={
        200: {
            "description": "Successful response with list of orders",
            "content": {
                "application/json": {
                    "example": {
                        "items": [
                            {
                                "id": 1,
                                "user_id": 1,
                                "status": "paid",
                                "created_at": "2024-01-15T10:30:00Z",
                                "items": [{"product_id": 1, "quantity": 2}],
                                "total_amount_cents": 3998,
                                "total_quantity": 2
                            }
                        ],
                        "total": 150,
                        "limit": 20,
                        "offset": 0,
                        "total_amount_cents": 500000,
                        "total_quantity": 250
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
```

**Pydantic Schema Examples**:
Add examples to Pydantic models for better Swagger documentation:

```python
class OrderCreate(BaseModel):
    user_id: int = Field(..., description="ID of the user placing the order", example=1)
    status: str = Field(default="pending", description="Order status", example="pending")
    items: List[OrderItemCreate] = Field(..., description="List of order items", min_items=1)
    
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
```

**Testing via Swagger UI**:
- All endpoints must be fully functional and testable directly from Swagger UI
- Request examples should be pre-filled and editable
- Response examples should be visible for all status codes
- Query parameters should have clear descriptions and example values
- All endpoints must work with the test database configuration

### 8.2 Postman Collection
- Generate Postman collection for all APIs
- Include all endpoints with example requests
- Organize into folders: Orders, Products, Users
- Include environment variables for base URL
- Include example responses
- Export as JSON file: `postman_collection.json`

### 8.3 Development Environment Setup
- Python 3.9 or higher
- Virtual environment (venv or conda)
- Install dependencies: `pip install -r requirements.txt`
- Install dev dependencies: `pip install -r requirements-dev.txt`
- Set up `.env` file with database credentials
- Run tests: `pytest`
- Run application: `uvicorn app.main:app --reload`

### 8.4 README.md Contents
- Project overview and purpose
- Prerequisites
- Installation instructions
- Environment setup
- Running the application
- Running tests
- API documentation links
- Project structure overview

## 9. Endpoint Verification and Completeness

### 9.1 Required Endpoints Checklist
All endpoints from the original requirements must be implemented and documented:

**Orders Endpoints**:
- [x] `GET /api/v1/orders` - List all orders
- [x] `GET /api/v1/orders?status={status}` - List orders by status (paid, shipped, cancelled, pending)
- [x] `GET /api/v1/orders?user_id={user_id}` - List orders by user
- [x] `GET /api/v1/orders?start_date={date}&end_date={date}` - List orders by date range
- [x] `GET /api/v1/orders?product_id={product_id}` - List orders by product
- [x] `POST /api/v1/orders` - Create a new order
- [x] `PATCH /api/v1/orders/{order_id}` - Update order status

**Products Endpoints**:
- [x] `GET /api/v1/products` - List all products
- [x] `POST /api/v1/products` - Add a new product
- [x] `PATCH /api/v1/products/{product_id}` - Update product name and/or price

**Users Endpoints**:
- [x] `GET /api/v1/users` - List all users
- [x] `PATCH /api/v1/users/{user_id}` - Update user email and/or full name

### 9.2 Aggregation Requirements Verification
- [x] Order list responses include `total_quantity` when quantity data is present
- [x] Order list responses include `total_amount_cents` when amount data is present
- [x] Aggregations are calculated across all filtered results, not just the current page

### 9.3 Swagger UI Testing Requirements
All endpoints must be:
- **Functional**: Testable and working via Swagger UI `/docs`
- **Documented**: Complete with descriptions, examples, and response schemas
- **Validated**: Proper input validation with clear error messages
- **Tested**: Verified to work with actual database connections

### 9.4 Postman Collection Requirements
- Include all 11 endpoints with proper organization
- Provide example requests for each endpoint
- Include environment variables for base URL configuration
- Include example responses for success and error cases
- Export as `postman_collection.json` in project root

## 10. Additional Implementation Notes

### 10.1 Order Creation Logic
When creating an order:
1. Validate user exists
2. For each item, validate product exists
3. Fetch current product price for each item
4. Store `price_cents_at_purchase` in order_items (snapshot of price at purchase time)
5. Calculate total amount and total quantity
6. Create order and order_items in a transaction

### 10.2 Filtering and Aggregation
- Implement filtering in repository layer using SQLAlchemy queries
- Use SQL aggregation functions (SUM, COUNT) for totals
- Ensure totals are calculated across all matching records, not just current page
- Use database indexes for efficient filtering (already present on user_id, order_id)

### 10.3 Date Filtering
- Accept ISO 8601 date strings
- Support date range filtering (start_date, end_date)
- Parse dates properly, handle timezone considerations
- Filter on `created_at` field for orders

### 10.4 Response Serialization
- Use Pydantic models for response serialization
- Include related data (e.g., order items in order response)
- Format dates as ISO 8601 strings
- Convert price_cents to appropriate format in responses

## 11. Dependencies

### 11.1 Core Dependencies
```
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
sqlalchemy>=2.0.0
psycopg2-binary>=2.9.0
pydantic>=2.0.0
pydantic-settings>=2.0.0
python-dotenv>=1.0.0
```

### 11.2 Development Dependencies
```
pytest>=7.4.0
pytest-asyncio>=0.21.0
pytest-cov>=4.1.0
black>=23.0.0
mypy>=1.5.0
```

---

## Document Status
This PRD document is ready for implementation. All code, comments, and documentation generated based on this PRD must be in English.

