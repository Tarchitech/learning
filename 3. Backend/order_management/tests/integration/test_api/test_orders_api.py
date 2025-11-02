"""
Integration tests for orders API endpoints.
"""
import pytest
from fastapi import status


def test_list_orders_empty(client):
    """Test listing orders when none exist."""
    response = client.get("/api/v1/orders")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["orders"]) == 0
    assert data["total_amount_cents"] == 0
    assert data["total_quantity"] == 0


def test_create_order_success(client, sample_user, sample_product):
    """Test creating an order via API."""
    order_data = {
        "user_id": sample_user.id,
        "status": "pending",
        "items": [
            {
                "product_id": sample_product.id,
                "quantity": 2
            }
        ]
    }
    response = client.post("/api/v1/orders", json=order_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["status"] == "pending"
    assert "order_id" in data
    assert len(data["items"]) == 1
    assert data["total_quantity"] == 2


def test_create_order_invalid_user(client, sample_product):
    """Test creating order with invalid user ID."""
    order_data = {
        "user_id": 999,
        "status": "pending",
        "items": [
            {
                "product_id": sample_product.id,
                "quantity": 1
            }
        ]
    }
    response = client.post("/api/v1/orders", json=order_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_order_status(client, sample_order):
    """Test updating order status via API."""
    update_data = {"status": "paid"}
    response = client.patch(f"/api/v1/orders/{sample_order.id}", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "paid"
    assert data["order_id"] == sample_order.id
    assert "updated_at" in data


def test_list_orders_with_filter(client, sample_order):
    """Test listing orders with status filter."""
    response = client.get("/api/v1/orders?status=pending")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["orders"]) >= 1
    assert "limit" in data
    assert "offset" in data

