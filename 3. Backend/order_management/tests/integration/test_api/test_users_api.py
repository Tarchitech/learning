"""
Integration tests for users API endpoints.
"""
import pytest
from fastapi import status


def test_list_users(client, sample_user):
    """Test listing users."""
    response = client.get("/api/v1/users")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total"] >= 1
    assert len(data["items"]) >= 1


def test_update_user(client, sample_user):
    """Test updating a user via API."""
    import uuid
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

