"""
Unit tests for product service.
"""
import pytest
from app.services.product_service import ProductService
from app.schemas.product import ProductCreate, ProductUpdate
from app.utils.exceptions import ProductNotFoundError, ValidationError


def test_get_product_success(db_session, sample_product):
    """Test successful product retrieval."""
    service = ProductService(db_session)
    result = service.get_product(sample_product.id)
    assert result.id == sample_product.id
    assert result.name == sample_product.name
    assert result.price_cents == sample_product.price_cents


def test_get_product_not_found(db_session):
    """Test product retrieval with invalid ID."""
    service = ProductService(db_session)
    with pytest.raises(ProductNotFoundError):
        service.get_product(999)


def test_create_product_success(db_session):
    """Test successful product creation."""
    service = ProductService(db_session)
    product_data = ProductCreate(name="New Product", price_cents=2999)
    result = service.create_product(product_data)
    assert result.id is not None
    assert result.name == "New Product"
    assert result.price_cents == 2999


def test_create_product_negative_price(db_session):
    """Test product creation with negative price."""
    from pydantic import ValidationError as PydanticValidationError
    service = ProductService(db_session)
    # Pydantic will raise validation error before service is called
    with pytest.raises(PydanticValidationError):
        ProductCreate(name="Product", price_cents=-100)


def test_update_product_success(db_session, sample_product):
    """Test successful product update."""
    service = ProductService(db_session)
    product_update = ProductUpdate(name="Updated Product", price_cents=2499)
    result = service.update_product(sample_product.id, product_update)
    assert result.name == "Updated Product"
    assert result.price_cents == 2499


def test_update_product_not_found(db_session):
    """Test product update with invalid ID."""
    service = ProductService(db_session)
    product_update = ProductUpdate(name="Updated Product")
    with pytest.raises(ProductNotFoundError):
        service.update_product(999, product_update)


def test_update_product_no_fields(db_session, sample_product):
    """Test product update with no fields provided."""
    service = ProductService(db_session)
    product_update = ProductUpdate()
    with pytest.raises(ValidationError):
        service.update_product(sample_product.id, product_update)

