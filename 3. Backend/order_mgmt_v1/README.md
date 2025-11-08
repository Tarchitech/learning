# Order Management System v1 - Simplified Version

A simplified database operations system for learning purposes. This version demonstrates core database concepts using SQLAlchemy ORM with a simple console interface.

## Overview

This is a beginner-friendly version of an order management system designed for teaching and learning database operations. The code is organized into separate modules to make it easier to understand while keeping the logic simple and straightforward. All database operations are performed through simple functions that can be called from a console interface.

## Features

- **Simple Structure**: Organized into separate modules - config, database, models, db_operations, and console
- **Create Users**: Register new users with email and full name
- **Create Products**: Add products to the catalog with name and price
- **Create Orders**: Place orders with multiple items (captures prices at purchase time)
- **List Orders**: View all orders for a specific user (includes user name and product names)
- **Console Interface**: Simple text-based interface for user interaction
- **PostgreSQL Database**: Uses PostgreSQL with SQLAlchemy ORM

## Technology Stack

- **ORM**: SQLAlchemy 2.0+
- **Database**: PostgreSQL
- **Language**: Python 3.8+

## Project Structure

```
order_mgmt_v1/
├── console.py          # Console interface for user input
├── db_operations.py    # Core database operation functions
├── database.py         # Database connection and session management
├── models.py           # SQLAlchemy ORM models (Users, Products, Orders, OrderItems)
├── requirements.txt    # Python dependencies
├── README.md           # This file
└── .gitignore          # Git ignore rules
```

## Setup Instructions

### 1. Prerequisites

- Python 3.8+
- PostgreSQL database (local or remote)
- pip (Python package manager)

### 2. Installation

```bash
# Navigate to the project directory
cd "learning/3. Backend/order_mgmt_v1"

# Create a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Database Configuration

Edit `database.py` and update the database connection string:

```python
engine = create_engine('postgresql://user:password@host:port/dbname?sslmode=require')
```

### 4. Generate Models (If Needed)

If you have an existing database and want to generate `models.py`:

```bash
# Install sqlacodegen
pip install sqlacodegen

# Generate models from existing database
sqlacodegen postgresql://user:password@host:port/dbname \
  --schema your-schema \
  --generator declarative \
  > models.py
```

**Note:** The generated models use SQLAlchemy 2.0 syntax. Make sure the `Base` class in `models.py` matches your setup, or update imports in `db_operations.py` accordingly.

### 5. Run the Console Interface

```bash
python console.py
```

The console interface will display a menu with the following options:
1. Create a new user
2. Create a new product
3. Create a new order
4. List orders for a user
5. Exit

## Core Database Operations

The system provides four core database operation functions in `db_operations.py`:

### 1. Create User

```python
from db_operations import create_user

result = create_user(
    email="user@example.com",
    full_name="John Doe"
)
# Returns: {"id": 1, "email": "user@example.com", "full_name": "John Doe", "created_at": "2024-01-10T08:00:00Z"}
```

### 2. Create Product

```python
from db_operations import create_product

result = create_product(
    name="MacBook Pro 16\"",
    price_cents=249999  # $2499.99
)
# Returns: {"id": 1, "name": "MacBook Pro 16\"", "price_cents": 249999}
```

### 3. Create Order

```python
from db_operations import create_order

result = create_order(
    user_id=1,
    status="pending",
    items=[
        {"product_id": 1, "quantity": 2},
        {"product_id": 2, "quantity": 1}
    ]
)
# Returns: Order dictionary with items and calculated totals
```

### 4. List Orders

```python
from db_operations import list_orders

result = list_orders(user_id=1)
# Returns: {"orders": [...], "total": 2}
```

## Architecture

### System Architecture

This simplified version uses a modular structure with direct database access:

```mermaid
flowchart TD
    Console[Console Interface<br/>console.py<br/>- User Input<br/>- Menu Display]
    
    DBOps[Database Operations<br/>db_operations.py<br/>- create_user<br/>- create_product<br/>- create_order<br/>- list_orders]
    
    Database[Database Module<br/>database.py<br/>- Connection Management<br/>- Session Factory]
    
    Models[Models Module<br/>models.py<br/>- User, Product<br/>- Order, OrderItem<br/>- Relationships]
    
    PostgreSQL[("PostgreSQL Database<br/>Schema: your-schema<br/>- users<br/>- products<br/>- orders<br/>- order_items")]
    
    Console -->|Calls Functions| DBOps
    DBOps -->|Uses Sessions| Database
    DBOps -->|Uses Models| Models
    Database -->|SQLAlchemy ORM| Models
    Models --> PostgreSQL
    
    style Console fill:#1e3a5f,stroke:#4a90e2,stroke-width:2px,color:#e8f4fd
    style DBOps fill:#3d2817,stroke:#d4a574,stroke-width:2px,color:#f5e6d3
    style Database fill:#3a1e4a,stroke:#b474d4,stroke-width:2px,color:#e8d4f5
    style Models fill:#4a1e1e,stroke:#d47474,stroke-width:2px,color:#f5d4d4
    style PostgreSQL fill:#1e1e4a,stroke:#7474d4,stroke-width:2px,color:#d4d4f5
```

### Request Flow

How a database operation flows through the system:

```mermaid
sequenceDiagram
    participant User
    participant Console as Console Interface<br/>(console.py)
    participant DBOps as Database Operations<br/>(db_operations.py)
    participant DB as Database<br/>Session
    participant Models as ORM Models
    participant PostgreSQL as PostgreSQL<br/>Database
    
    User->>Console: Enter Input
    Console->>DBOps: Call Function<br/>(e.g., create_user)
    DBOps->>DB: Create Session
    DBOps->>Models: Create ORM Object
    DBOps->>DB: Add & Commit
    DB->>PostgreSQL: Execute SQL
    PostgreSQL-->>DB: Return Results
    DB-->>DBOps: ORM Object with ID
    DBOps->>DB: Close Session
    DBOps-->>Console: Return Dictionary
    Console-->>User: Display Result
```

### Create Order Flow

Detailed flow for creating an order:

```mermaid
sequenceDiagram
    participant User
    participant Console as Console Interface
    participant DBOps as create_order()
    participant DB as Database Session
    participant PostgreSQL
    
    User->>Console: Enter Order Data<br/>(user_id, status, items)
    Console->>DBOps: Call create_order()
    DBOps->>DB: Create Session
    DBOps->>DB: Create Order Object<br/>db.add(db_order)
    DBOps->>DB: Flush (get order ID)<br/>db.flush()
    loop For Each Item
        DBOps->>DB: Query Product<br/>to get current price
        DB->>PostgreSQL: SELECT product WHERE id = ?
        PostgreSQL-->>DB: Product Data
        DB-->>DBOps: Product Object
        DBOps->>DBOps: Calculate Price<br/>price_cents * quantity
        DBOps->>DB: Create OrderItem<br/>with captured price
        DBOps->>DB: Add OrderItem to Session
    end
    DBOps->>DB: Commit Transaction<br/>db.commit()
    DB->>PostgreSQL: INSERT order<br/>INSERT order_items
    PostgreSQL-->>DB: Records Created
    DB-->>DBOps: Order with Items
    DBOps->>DBOps: Calculate Totals<br/>(sum amounts & quantities)
    DBOps->>DB: Close Session
    DBOps-->>Console: Return Order Dictionary
    Console-->>User: Display Order Details
```

### Database Schema

Database relationships:

```mermaid
erDiagram
    USERS ||--o{ ORDERS : "has"
    ORDERS ||--o{ ORDER_ITEMS : "contains"
    PRODUCTS ||--o{ ORDER_ITEMS : "referenced_in"
    
    USERS {
        int id PK
        string email UK
        string full_name
        datetime created_at
    }
    
    PRODUCTS {
        int id PK
        string name
        int price_cents
    }
    
    ORDERS {
        int id PK
        int user_id FK
        string status
        datetime created_at
    }
    
    ORDER_ITEMS {
        int id PK
        int order_id FK
        int product_id FK
        int quantity
        int price_cents_at_purchase
    }
```

## Key Concepts Demonstrated

### 1. SQLAlchemy ORM
- Model definitions with relationships (User-Order, Order-OrderItem, Product-OrderItem)
- Foreign key constraints for data integrity
- Database session management
- Automatic table creation
- Eager loading with `joinedload` to prevent N+1 queries

### 2. Database Operations
- Direct ORM queries in functions (no service/repository layers)
- Transaction management (commit/rollback)
- Relationship loading (user, products via SQLAlchemy relationships)
- Price capture at purchase time (stored in order_items)

### 3. Console Interface
- Simple text-based user interaction
- Input validation and error handling
- Menu-driven navigation
- Clear output formatting

## Code Structure

### Module Responsibilities

- **database.py**: Creates SQLAlchemy engine and provides `get_db()` function for database sessions
- **models.py**: Defines ORM models (Users, Products, Orders, OrderItems) with relationships. Can be manually written or generated using `sqlacodegen` from existing database
- **db_operations.py**: Contains the four core database operation functions
- **console.py**: Provides console interface for user interaction

### How to Generate models.py

If you have an existing PostgreSQL database, you can automatically generate `models.py`:

1. **Install sqlacodegen:**
   ```bash
   pip install sqlacodegen
   ```

2. **Generate models:**
   ```bash
   sqlacodegen postgresql://user:password@host:port/dbname \
     --schema your-schema \
     --generator declarative \
     > models.py
   ```

3. **Update imports if needed:**
   - The generated models include their own `Base` class
   - Update `db_operations.py` to use the correct model names (Users, Products, Orders, OrderItems)

### Function Signatures

```python
# Create a new user
def create_user(email: str, full_name: str) -> dict

# Create a new product
def create_product(name: str, price_cents: int) -> dict

# Create a new order
def create_order(user_id: int, status: str, items: list) -> dict

# List orders for a user
def list_orders(user_id: int) -> dict
```

## Learning Path

This simplified version is designed to help beginners understand:

1. **Database Basics**: How to connect to PostgreSQL using SQLAlchemy
2. **ORM Concepts**: Using SQLAlchemy ORM for database operations
3. **Database Operations**: Creating, reading, and managing data
4. **ORM Relationships**: How to define and use relationships between models
5. **Transaction Management**: Creating related records in a single transaction
6. **Console Programming**: Building simple text-based interfaces

Once comfortable with this version, you can progress to:
- Understanding layered architecture
- Service layer separation
- Repository pattern
- Advanced querying and filtering
- Web API development (FastAPI, Flask, etc.)
- Testing strategies

## Common Issues and Solutions

### Database Connection Error

**Problem**: Cannot connect to PostgreSQL

**Solutions**:
1. Verify database connection string in `database.py` is correct
2. Ensure PostgreSQL is running
3. Check database and schema exist
4. For Neon.tech, ensure `?sslmode=require` is included in connection string
5. Verify network connectivity if using remote database

### Table Creation Issues

**Problem**: Tables not found

**Solutions**:
1. Ensure schema exists: `CREATE SCHEMA IF NOT EXISTS your-schema;`
2. If tables don't exist, create them manually or use SQLAlchemy's `Base.metadata.create_all()`
3. If using generated models, ensure they match your database schema
4. Review error messages for specific issues

### Database Constraint Errors

**Problem**: Unique constraint violations or foreign key errors

**Solutions**:
1. Email must be unique - check if user already exists
2. User ID must exist when creating orders
3. Product ID must exist when creating order items
4. Check database logs for specific constraint violations

## Next Steps

After understanding this simplified version:

1. **Add Error Handling**: Improve error messages and validation
2. **Add Tests**: Write unit and integration tests
3. **Add More Operations**: Implement update and delete functions
4. **Add Filtering**: Add more filtering options for list operations
5. **Refactor to Layers**: Separate into service/repository layers
6. **Build Web API**: Create REST API using FastAPI or Flask

## Resources

- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Python Documentation](https://docs.python.org/)

## License

This is a learning/teaching project.
