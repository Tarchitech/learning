"""
Integration tests for products API endpoints.
"""
import pytest
from fastapi import status


def test_list_products_empty(client, db_session):
    """Test listing products when none exist."""
    # Clear all products first
    from app.models.product import Product
    db_session.query(Product).delete()
    db_session.commit()
    
    response = client.get("/api/v1/products")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total"] == 0
    assert len(data["items"]) == 0


def test_list_products_with_data(client, sample_product):
    """Test listing products with existing data."""
    response = client.get("/api/v1/products")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total"] >= 1
    assert len(data["items"]) >= 1


def test_get_product_by_id(client, sample_product):
    """Test getting a product by ID."""
    response = client.get(f"/api/v1/products/{sample_product.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == sample_product.id
    assert data["name"] == sample_product.name
    assert data["price_cents"] == sample_product.price_cents


def test_get_product_by_id_not_found(client):
    """Test getting a non-existent product by ID."""
    response = client.get("/api/v1/products/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_product(client):
    """Test creating a product."""
    product_data = {
        "name": "New Product",
        "price_cents": 2999
    }
    response = client.post("/api/v1/products", json=product_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "New Product"
    assert data["price_cents"] == 2999


def test_create_product_negative_price(client):
    """Test creating product with negative price."""
    product_data = {
        "name": "Invalid Product",
        "price_cents": -100
    }
    response = client.post("/api/v1/products", json=product_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_product_empty_name(client):
    """Test creating product with empty name."""
    product_data = {
        "name": "",
        "price_cents": 1000
    }
    response = client.post("/api/v1/products", json=product_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_product(client, sample_product):
    """Test updating a product."""
    update_data = {
        "name": "Updated Product",
        "price_cents": 2499
    }
    response = client.patch(f"/api/v1/products/{sample_product.id}", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Updated Product"
    assert data["price_cents"] == 2499


def test_update_product_not_found(client):
    """Test updating a non-existent product."""
    update_data = {
        "name": "Updated Product",
        "price_cents": 2499
    }
    response = client.patch("/api/v1/products/99999", json=update_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_product_partial(client, sample_product):
    """Test updating a product with partial data."""
    update_data = {
        "name": "Partially Updated Product"
    }
    response = client.patch(f"/api/v1/products/{sample_product.id}", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Partially Updated Product"
    # Price should remain unchanged
    assert data["price_cents"] == sample_product.price_cents


def test_update_product_no_fields(client, sample_product):
    """Test updating a product with no fields."""
    update_data = {}
    response = client.patch(f"/api/v1/products/{sample_product.id}", json=update_data)
    # Should fail validation
    assert response.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_422_UNPROCESSABLE_ENTITY]
