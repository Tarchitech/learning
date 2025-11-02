"""
Integration tests for products API endpoints.
"""
import pytest
from fastapi import status


def test_list_products(client, sample_product):
    """Test listing products."""
    response = client.get("/api/v1/products")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total"] >= 1
    assert len(data["items"]) >= 1


def test_create_product(client):
    """Test creating a product via API."""
    product_data = {
        "name": "New Product",
        "price_cents": 2999
    }
    response = client.post("/api/v1/products", json=product_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "New Product"
    assert data["price_cents"] == 2999


def test_update_product(client, sample_product):
    """Test updating a product via API."""
    update_data = {
        "name": "Updated Product",
        "price_cents": 2499
    }
    response = client.patch(f"/api/v1/products/{sample_product.id}", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Updated Product"
    assert data["price_cents"] == 2499

