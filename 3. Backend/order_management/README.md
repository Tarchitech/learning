# Order Management System

A comprehensive REST API for managing orders, products, and users built with FastAPI, SQLAlchemy, and PostgreSQL.

## Features

- **Order Management**: Create, list, and update orders with multi-dimensional filtering
- **Product Catalog**: Manage product information with name and price updates
- **User Management**: Update user email and full name
- **Aggregation Support**: Total quantity and total amount calculations across filtered results
- **Comprehensive Filtering**: Filter orders by status, user, date range, or product
- **RESTful API**: Following REST principles with proper HTTP status codes
- **Auto-Generated Documentation**: Swagger/OpenAPI documentation at `/docs`
- **Type Safety**: Full type hints and Pydantic validation
- **Test Coverage**: Unit and integration tests

## Technology Stack

- **Framework**: FastAPI 0.104+
- **ORM**: SQLAlchemy 2.0+
- **Validation**: Pydantic 2.0+
- **Database**: PostgreSQL (via Neon.tech)
- **Testing**: pytest with pytest-asyncio
- **API Documentation**: FastAPI auto-generated Swagger/OpenAPI

## Project Structure

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
│   │   └── deps.py                # API dependencies
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py              # Configuration management
│   │   ├── database.py            # Database connection and session
│   │   └── security.py            # Security utilities
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py                # Base model class
│   │   ├── user.py                # User ORM model
│   │   ├── order.py               # Order ORM model
│   │   ├── product.py             # Product ORM model
│   │   └── order_item.py          # OrderItem ORM model
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── order.py               # Order Pydantic schemas
│   │   ├── product.py             # Product Pydantic schemas
│   │   └── user.py                # User Pydantic schemas
│   ├── services/
│   │   ├── __init__.py
│   │   ├── order_service.py       # Order business logic
│   │   ├── product_service.py     # Product business logic
│   │   └── user_service.py       # User business logic
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── base.py                # Base repository
│   │   ├── order_repository.py    # Order data access
│   │   ├── product_repository.py  # Product data access
│   │   └── user_repository.py    # User data access
│   └── utils/
│       ├── __init__.py
│       ├── exceptions.py          # Custom exceptions
│       └── helpers.py             # Helper functions
├── tests/
│   ├── __init__.py
│   ├── conftest.py                # pytest configuration
│   ├── unit/
│   │   ├── test_services/          # Service unit tests
│   │   ├── test_repositories/    # Repository unit tests
│   │   └── test_utils/            # Utility tests
│   ├── integration/
│   │   └── test_api/              # API integration tests
│   └── fixtures/                  # Test fixtures
├── docs/
│   ├── ARCHITECTURE.md            # Architecture diagrams
│   ├── SEQUENCE.md                # Sequence diagrams
│   ├── order_management_prd.md    # Product requirements document
│   └── prd_init.md                # Initial PRD
├── scripts/
│   └── add_updated_at_column.py  # Database migration script
├── migrations/
│   └── add_updated_at_column.sql  # SQL migration script
├── postman_collection.json        # Postman API collection
├── .env.example                   # Environment variables template
├── .gitignore
├── requirements.txt               # Production dependencies
├── requirements-dev.txt           # Development dependencies
├── pytest.ini                     # pytest configuration
└── README.md                       # This file
```

## Prerequisites

- Python 3.9 or higher
- PostgreSQL database (or use Neon.tech)
- pip (Python package manager)

## Installation

1. **Clone the repository** (if applicable) or navigate to the project directory:
   ```bash
   cd order_management
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # For development
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` file with your database credentials:
   ```env
   DB_HOST=your-database-host
   DB_PORT=5432
   DB_NAME=your-database-name
   DB_USER=your-username
   DB_PASSWORD=your-password
   DB_SCHEMA=tony
   API_V1_PREFIX=/api/v1
   DEBUG=False
   LOG_LEVEL=INFO
   ```

5. **Database Setup**:
   Ensure the database schema is created. The SQL schema is provided in `docs/prd_init.md`.
   
   **Important**: Run the migration script to add the `updated_at` column to the orders table:
   ```bash
   python3 scripts/add_updated_at_column.py
   ```
   
   Or manually run the SQL migration:
   ```sql
   ALTER TABLE tony.orders ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITH TIME ZONE;
   ```

## Running the Application

**Development mode**:
```bash
uvicorn app.main:app --reload
```

The API will be available at:
- **API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

**Production mode**:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

### Orders

- `GET /api/v1/orders` - List orders (supports filtering by status, user_id, date range, product_id)
- `POST /api/v1/orders` - Create a new order
- `PATCH /api/v1/orders/{order_id}` - Update order status

### Products

- `GET /api/v1/products` - List all products
- `GET /api/v1/products/{product_id}` - Get product by ID (full information)
- `POST /api/v1/products` - Create a new product
- `PATCH /api/v1/products/{product_id}` - Update product name and/or price

### Users

- `GET /api/v1/users` - List all users
- `GET /api/v1/users/{user_id}` - Get user by ID (full information)
- `PATCH /api/v1/users/{user_id}` - Update user email and/or full name

For detailed API documentation, visit `/docs` when the application is running.

## Example Requests

### Create an Order

```bash
curl -X POST "http://localhost:8000/api/v1/orders" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "status": "pending",
    "items": [
      {"product_id": 1, "quantity": 2},
      {"product_id": 2, "quantity": 1}
    ]
  }'
```

**Response:**
```json
{
  "order_id": 1,
  "user_id": 1,
  "user_name": "John Doe",
  "status": "pending",
  "created_at": "2024-01-16T10:30:00Z",
  "items": [
    {
      "id": 1,
      "product_id": 1,
      "quantity": 2,
      "price_cents_at_purchase": 249999,
      "product_name": "MacBook Pro 16\""
    }
  ],
  "total_amount_cents": 499998,
  "total_quantity": 2
}
```

### List Orders with Filters

```bash
curl "http://localhost:8000/api/v1/orders?status=paid&user_id=1&limit=20&offset=0"
```

**Response format:**
```json
{
  "orders": [
    {
      "order_id": 1,
      "user_id": 1,
      "user_name": "John Doe",
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
```

### Get Product by ID

```bash
curl "http://localhost:8000/api/v1/products/1"
```

**Response:**
```json
{
  "id": 1,
  "name": "MacBook Pro 16\"",
  "price_cents": 249999
}
```

### Get User by ID

```bash
curl "http://localhost:8000/api/v1/users/1"
```

**Response:**
```json
{
  "id": 1,
  "email": "john.doe@example.com",
  "full_name": "John Doe",
  "created_at": "2024-01-10T08:00:00Z"
}
```

### Update Product

```bash
curl -X PATCH "http://localhost:8000/api/v1/products/1" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Product Name",
    "price_cents": 2499
  }'
```

### Update Order Status

```bash
curl -X PATCH "http://localhost:8000/api/v1/orders/1" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "paid"
  }'
```

**Response:**
```json
{
  "order_id": 1,
  "user_id": 1,
  "status": "paid",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T11:00:00Z"
}
```

## Running Tests

**Run all tests**:
```bash
pytest
```

**Run with coverage**:
```bash
pytest --cov=app --cov-report=html
```

**Run specific test file**:
```bash
pytest tests/unit/test_services/test_order_service.py
```

**Run integration tests only**:
```bash
pytest tests/integration/ -v
```

## Architecture

The application follows a layered architecture:

1. **API Layer**: Handles HTTP requests/responses
2. **Service Layer**: Contains business logic
3. **Repository Layer**: Data access abstraction
4. **Model Layer**: SQLAlchemy ORM models
5. **Schema Layer**: Pydantic models for validation

See `docs/ARCHITECTURE.md` and `docs/SEQUENCE.md` for detailed architecture and sequence diagrams.

## Security Best Practices

- Input validation using Pydantic schemas
- SQL injection prevention via SQLAlchemy ORM
- Environment variables for sensitive data
- CORS middleware configuration
- Error handling without information leakage

## Testing Strategy

- **Unit Tests**: Test services and repositories in isolation
- **Integration Tests**: Test API endpoints with test database
- **Coverage Target**: Minimum 80% code coverage

## Development

**Code Style**:
- Follow PEP 8
- Use type hints for all functions
- Include docstrings (Google style)
- Maximum line length: 88 characters (Black default)

**Before committing**:
```bash
# Format code
black app/ tests/

# Run tests
pytest

# Check types (optional)
mypy app/
```

## API Documentation

- **Swagger UI**: Interactive API documentation at `/docs`
- **ReDoc**: Alternative documentation at `/redoc`
- **OpenAPI JSON**: Schema at `/openapi.json`

All endpoints are documented with:
- Request/response examples
- Parameter descriptions
- Error response schemas
- Status code documentation

## Database Schema

The system uses PostgreSQL with the following schema:

- **Schema**: `tony`
- **Tables**:
  - `users`: User information
  - `orders`: Order headers
  - `products`: Product catalog
  - `order_items`: Order line items

See `docs/prd_init.md` for the complete SQL schema.

## Error Handling

All errors follow a consistent format:

```json
{
  "detail": "Error message describing what went wrong",
  "code": "ERROR_CODE"
}
```

Common HTTP status codes:
- `200 OK`: Success
- `201 Created`: Resource created
- `400 Bad Request`: Validation error
- `404 Not Found`: Resource not found
- `409 Conflict`: Duplicate resource
- `500 Internal Server Error`: Server error

## Contributing

1. Follow the coding standards outlined in the PRD
2. Write tests for new features
3. Update documentation as needed
4. Ensure all tests pass before submitting

## License

This project is part of a learning exercise.

## Support

For issues or questions, refer to the PRD document in `docs/order_management_prd.md`.

---

**Note**: Ensure your database credentials in `.env` are correct and the database schema is set up before running the application.

