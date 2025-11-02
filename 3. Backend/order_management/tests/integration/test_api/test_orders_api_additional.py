"""
Additional integration tests for orders API endpoints.
"""
import pytest
from fastapi import status


# Note: There is no GET /orders/{order_id} endpoint, orders are retrieved via list endpoint
# This test is removed as the endpoint doesn't exist


def test_create_order_invalid_product(client, sample_user):
    """Test creating order with invalid product ID."""
    order_data = {
        "user_id": sample_user.id,
        "status": "pending",
        "items": [
            {
                "product_id": 99999,
                "quantity": 1
            }
        ]
    }
    response = client.post("/api/v1/orders", json=order_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_order_empty_items(client, sample_user, sample_product):
    """Test creating order with empty items list."""
    order_data = {
        "user_id": sample_user.id,
        "status": "pending",
        "items": []
    }
    response = client.post("/api/v1/orders", json=order_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_order_invalid_status(client, sample_user, sample_product):
    """Test creating order with invalid status."""
    order_data = {
        "user_id": sample_user.id,
        "status": "invalid_status",
        "items": [
            {
                "product_id": sample_product.id,
                "quantity": 1
            }
        ]
    }
    response = client.post("/api/v1/orders", json=order_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_update_order_status_invalid_status(client, sample_order):
    """Test updating order with invalid status."""
    update_data = {"status": "invalid_status"}
    response = client.patch(f"/api/v1/orders/{sample_order.id}", json=update_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_list_orders_with_product_filter(client, sample_order, sample_product):
    """Test listing orders filtered by product_id."""
    # Create an order item with the product
    response = client.get(f"/api/v1/orders?product_id={sample_product.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "orders" in data
    assert "total_amount_cents" in data
    assert "total_quantity" in data


def test_list_orders_with_date_range(client, sample_order):
    """Test listing orders with date range filter."""
    response = client.get(
        "/api/v1/orders?start_date=2024-01-01T00:00:00Z&end_date=2024-12-31T23:59:59Z"
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "orders" in data


def test_list_orders_pagination(client, sample_order):
    """Test listing orders with pagination."""
    response = client.get("/api/v1/orders?limit=1&offset=0")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["limit"] == 1
    assert data["offset"] == 0
    assert len(data["orders"]) <= 1


def test_list_orders_invalid_status(client):
    """Test listing orders with invalid status filter."""
    response = client.get("/api/v1/orders?status=invalid")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_create_order_with_multiple_items(client, sample_user, sample_product, db_session):
    """Test creating order with multiple items."""
    # Create another product
    from app.models.product import Product
    product2 = Product(name="Product 2", price_cents=1999)
    db_session.add(product2)
    db_session.commit()
    
    order_data = {
        "user_id": sample_user.id,
        "status": "pending",
        "items": [
            {
                "product_id": sample_product.id,
                "quantity": 2
            },
            {
                "product_id": product2.id,
                "quantity": 1
            }
        ]
    }
    response = client.post("/api/v1/orders", json=order_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert len(data["items"]) == 2
    assert data["total_quantity"] == 3

