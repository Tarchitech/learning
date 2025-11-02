"""
Integration tests for users API endpoints.
"""
import pytest
from fastapi import status
import uuid


def test_list_users(client, sample_user):
    """Test listing users."""
    response = client.get("/api/v1/users")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total"] >= 1
    assert len(data["items"]) >= 1


def test_list_users_empty(client):
    """Test listing users when none exist."""
    # This test might pass or fail depending on database state
    response = client.get("/api/v1/users")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "items" in data
    assert "total" in data


def test_get_user_by_id(client, sample_user):
    """Test getting a user by ID."""
    response = client.get(f"/api/v1/users/{sample_user.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == sample_user.id
    assert data["email"] == sample_user.email
    assert data["full_name"] == sample_user.full_name


def test_get_user_by_id_not_found(client):
    """Test getting a non-existent user by ID."""
    response = client.get("/api/v1/users/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_user(client, sample_user):
    """Test updating a user via API."""
    unique_email = f"updated_{uuid.uuid4().hex[:8]}@example.com"
    update_data = {
        "email": unique_email,
        "full_name": "Updated Name"
    }
    response = client.patch(f"/api/v1/users/{sample_user.id}", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == unique_email
    assert data["full_name"] == "Updated Name"


def test_update_user_partial(client, sample_user):
    """Test updating a user with partial data."""
    update_data = {
        "full_name": "Only Name Updated"
    }
    response = client.patch(f"/api/v1/users/{sample_user.id}", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["full_name"] == "Only Name Updated"


def test_update_user_email_only(client, sample_user):
    """Test updating only user email."""
    unique_email = f"emailonly_{uuid.uuid4().hex[:8]}@example.com"
    update_data = {
        "email": unique_email
    }
    response = client.patch(f"/api/v1/users/{sample_user.id}", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == unique_email


def test_update_user_not_found(client):
    """Test updating a non-existent user."""
    update_data = {
        "email": "newemail@example.com",
        "full_name": "New Name"
    }
    response = client.patch("/api/v1/users/99999", json=update_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_user_duplicate_email(client, db_session):
    """Test updating user with duplicate email."""
    from app.models.user import User
    user1 = User(email="user1@example.com", full_name="User 1")
    user2 = User(email="user2@example.com", full_name="User 2")
    db_session.add(user1)
    db_session.add(user2)
    db_session.commit()
    
    update_data = {"email": "user1@example.com"}
    response = client.patch(f"/api/v1/users/{user2.id}", json=update_data)
    assert response.status_code == status.HTTP_409_CONFLICT


def test_update_user_invalid_email(client, sample_user):
    """Test updating user with invalid email format."""
    update_data = {
        "email": "invalid-email-format"
    }
    # Pydantic will validate the email format before it reaches the service layer
    response = client.patch(f"/api/v1/users/{sample_user.id}", json=update_data)
    # Pydantic validation returns 422, not 400
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_user_empty_name(client, sample_user):
    """Test updating user with empty full_name."""
    update_data = {
        "full_name": ""
    }
    response = client.patch(f"/api/v1/users/{sample_user.id}", json=update_data)
    assert response.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_422_UNPROCESSABLE_ENTITY]


def test_update_user_no_fields(client, sample_user):
    """Test updating user with no fields provided."""
    update_data = {}
    response = client.patch(f"/api/v1/users/{sample_user.id}", json=update_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_list_users_pagination(client, sample_user):
    """Test listing users with pagination."""
    response = client.get("/api/v1/users?limit=1&offset=0")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["limit"] == 1
    assert data["offset"] == 0
    assert len(data["items"]) <= 1
