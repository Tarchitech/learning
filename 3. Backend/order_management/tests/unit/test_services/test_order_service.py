"""
Unit tests for order service.
"""
import pytest
from unittest.mock import Mock, patch
from app.services.order_service import OrderService
from app.schemas.order import OrderCreate, OrderUpdate
from app.utils.exceptions import OrderNotFoundError, UserNotFoundError, ProductNotFoundError, ValidationError


def test_get_order_success(db_session, sample_order):
    """Test successful order retrieval."""
    service = OrderService(db_session)
    result = service.get_order(sample_order.id)
    assert result.order_id == sample_order.id
    assert result.user_id == sample_order.user_id
    assert result.status == sample_order.status


def test_get_order_not_found(db_session):
    """Test order retrieval with invalid ID."""
    service = OrderService(db_session)
    with pytest.raises(OrderNotFoundError):
        service.get_order(999)


def test_create_order_success(db_session, sample_user, sample_product):
    """Test successful order creation."""
    from app.schemas.order import OrderItemCreate
    service = OrderService(db_session)
    order_data = OrderCreate(
        user_id=sample_user.id,
        status="pending",
        items=[OrderItemCreate(product_id=sample_product.id, quantity=2)]
    )
    result = service.create_order(order_data)
    assert result.order_id is not None
    assert result.status == "pending"
    assert len(result.items) == 1
    assert result.items[0].quantity == 2


def test_create_order_invalid_user(db_session, sample_product):
    """Test order creation with invalid user ID."""
    from app.schemas.order import OrderItemCreate
    service = OrderService(db_session)
    order_data = OrderCreate(
        user_id=999,
        status="pending",
        items=[OrderItemCreate(product_id=sample_product.id, quantity=2)]
    )
    with pytest.raises(UserNotFoundError):
        service.create_order(order_data)


def test_create_order_invalid_product(db_session, sample_user):
    """Test order creation with invalid product ID."""
    from app.schemas.order import OrderItemCreate
    service = OrderService(db_session)
    order_data = OrderCreate(
        user_id=sample_user.id,
        status="pending",
        items=[OrderItemCreate(product_id=999, quantity=2)]
    )
    with pytest.raises(ProductNotFoundError):
        service.create_order(order_data)


def test_create_order_invalid_status(db_session, sample_user, sample_product):
    """Test order creation with invalid status."""
    from app.schemas.order import OrderItemCreate
    service = OrderService(db_session)
    order_data = OrderCreate(
        user_id=sample_user.id,
        status="invalid_status",
        items=[OrderItemCreate(product_id=sample_product.id, quantity=2)]
    )
    with pytest.raises(ValidationError):
        service.create_order(order_data)


def test_update_order_status_success(db_session, sample_order):
    """Test successful order status update."""
    service = OrderService(db_session)
    order_update = OrderUpdate(status="paid")
    result = service.update_order_status(sample_order.id, order_update)
    assert result.status == "paid"


def test_update_order_status_not_found(db_session):
    """Test order status update with invalid ID."""
    service = OrderService(db_session)
    order_update = OrderUpdate(status="paid")
    with pytest.raises(OrderNotFoundError):
        service.update_order_status(999, order_update)


def test_update_order_status_invalid_status(db_session, sample_order):
    """Test order status update with invalid status."""
    service = OrderService(db_session)
    order_update = OrderUpdate(status="invalid_status")
    with pytest.raises(ValidationError):
        service.update_order_status(sample_order.id, order_update)

