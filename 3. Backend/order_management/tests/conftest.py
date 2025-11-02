"""
Pytest configuration and fixtures.
"""
import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from app.core.database import Base, get_db
from app.main import app
from app.models.user import User
from app.models.product import Product
from app.models.order import Order
from app.models.order_item import OrderItem

# Test database URL (in-memory SQLite for testing)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Event listener to modify DDL and remove schema references
@event.listens_for(engine, "before_cursor_execute", retval=True)
def receive_before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    """Modify SQL statements to remove schema references for SQLite."""
    if statement and isinstance(statement, str):
        # Remove schema references from all SQL statements
        # Remove schema prefixes like "tony."
        statement = statement.replace('tony.', '')
        # Fix foreign key references
        statement = statement.replace('tony.users.id', 'users.id')
        statement = statement.replace('tony.orders.id', 'orders.id')
        statement = statement.replace('tony.products.id', 'products.id')
        
        # Add IF NOT EXISTS to CREATE TABLE to avoid errors if table already exists
        if 'CREATE TABLE' in statement.upper() and 'IF NOT EXISTS' not in statement.upper():
            statement = statement.replace('CREATE TABLE', 'CREATE TABLE IF NOT EXISTS', 1)
        
        # Add IF NOT EXISTS to CREATE INDEX to avoid errors
        if 'CREATE INDEX' in statement.upper() and 'IF NOT EXISTS' not in statement.upper():
            statement = statement.replace('CREATE INDEX', 'CREATE INDEX IF NOT EXISTS', 1)
        
        # Add IF NOT EXISTS to CREATE UNIQUE INDEX to avoid errors
        if 'CREATE UNIQUE INDEX' in statement.upper() and 'IF NOT EXISTS' not in statement.upper():
            statement = statement.replace('CREATE UNIQUE INDEX', 'CREATE UNIQUE INDEX IF NOT EXISTS', 1)
    return statement, parameters

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """
    Create a test database session.
    
    Yields:
        Session: Test database session
    """
    # Remove schema from __table_args__ for SQLite compatibility
    original_table_args = {}
    for model in [User, Product, Order, OrderItem]:
        original_table_args[model] = model.__table_args__
        if model.__table_args__:
            if isinstance(model.__table_args__, tuple):
                # Filter out schema dict
                filtered = tuple(
                    arg for arg in model.__table_args__
                    if not (isinstance(arg, dict) and 'schema' in arg)
                )
                model.__table_args__ = filtered if filtered else None
            elif isinstance(model.__table_args__, dict):
                model.__table_args__ = {k: v for k, v in model.__table_args__.items() if k != 'schema'} or None
    
    # Create tables (event listener will modify SQL to remove schema)
    # Drop all first to ensure clean state
    try:
        Base.metadata.drop_all(bind=engine)
    except Exception:
        pass  # Ignore errors if tables don't exist
    Base.metadata.create_all(bind=engine)
    
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
        # Restore original table args
        for model, args in original_table_args.items():
            model.__table_args__ = args


@pytest.fixture(scope="function")
def client(db_session):
    """
    Create a test client.
    
    Args:
        db_session: Database session fixture
        
    Yields:
        TestClient: FastAPI test client
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def sample_user(db_session):
    """Create a sample user for testing."""
    import uuid
    unique_email = f"test_{uuid.uuid4().hex[:8]}@example.com"
    user = User(
        email=unique_email,
        full_name="Test User"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def sample_product(db_session):
    """Create a sample product for testing."""
    import uuid
    product = Product(
        name=f"Test Product {uuid.uuid4().hex[:4]}",
        price_cents=1999
    )
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)
    return product


@pytest.fixture
def sample_order(db_session, sample_user, sample_product):
    """Create a sample order for testing."""
    order = Order(
        user_id=sample_user.id,
        status="pending"
    )
    db_session.add(order)
    db_session.flush()
    
    order_item = OrderItem(
        order_id=order.id,
        product_id=sample_product.id,
        quantity=2,
        price_cents_at_purchase=sample_product.price_cents
    )
    db_session.add(order_item)
    db_session.commit()
    db_session.refresh(order)
    return order
