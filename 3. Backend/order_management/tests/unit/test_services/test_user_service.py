"""
Unit tests for user service.
"""
import pytest
from app.services.user_service import UserService
from app.schemas.user import UserUpdate
from app.utils.exceptions import UserNotFoundError, DuplicateEmailError, ValidationError


def test_get_user_success(db_session, sample_user):
    """Test successful user retrieval."""
    service = UserService(db_session)
    result = service.get_user(sample_user.id)
    assert result.id == sample_user.id
    assert result.email == sample_user.email
    assert result.full_name == sample_user.full_name


def test_get_user_not_found(db_session):
    """Test user retrieval with invalid ID."""
    service = UserService(db_session)
    with pytest.raises(UserNotFoundError):
        service.get_user(999)


def test_update_user_success(db_session, sample_user):
    """Test successful user update."""
    import uuid
    service = UserService(db_session)
    unique_email = f"newemail_{uuid.uuid4().hex[:8]}@example.com"
    user_update = UserUpdate(email=unique_email, full_name="New Name")
    result = service.update_user(sample_user.id, user_update)
    assert result.email == unique_email
    assert result.full_name == "New Name"


def test_update_user_not_found(db_session):
    """Test user update with invalid ID."""
    service = UserService(db_session)
    user_update = UserUpdate(email="newemail@example.com")
    with pytest.raises(UserNotFoundError):
        service.update_user(999, user_update)


def test_update_user_duplicate_email(db_session, sample_user):
    """Test user update with duplicate email."""
    # Create another user
    from app.models.user import User
    other_user = User(email="other@example.com", full_name="Other User")
    db_session.add(other_user)
    db_session.commit()
    
    service = UserService(db_session)
    user_update = UserUpdate(email=sample_user.email)  # Use existing email
    with pytest.raises(DuplicateEmailError):
        service.update_user(other_user.id, user_update)


def test_update_user_no_fields(db_session, sample_user):
    """Test user update with no fields provided."""
    service = UserService(db_session)
    user_update = UserUpdate()
    with pytest.raises(ValidationError):
        service.update_user(sample_user.id, user_update)

