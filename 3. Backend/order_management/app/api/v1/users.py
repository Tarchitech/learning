"""
User-related API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.services.user_service import UserService
from app.schemas.user import UserUpdate, UserResponse, UserListResponse
from app.utils.exceptions import UserNotFoundError, DuplicateEmailError, ValidationError

router = APIRouter()


@router.get(
    "/users",
    response_model=UserListResponse,
    summary="List users",
    description="Retrieve a list of all users with pagination.",
    tags=["users"],
    responses={
        200: {
            "description": "Successful response with list of users",
            "content": {
                "application/json": {
                    "example": {
                        "items": [
                            {
                                "id": 1,
                                "email": "user@example.com",
                                "full_name": "John Doe",
                                "created_at": "2024-01-10T08:00:00Z"
                            }
                        ],
                        "total": 100,
                        "limit": 20,
                        "offset": 0
                    }
                }
            }
        },
        500: {
            "description": "Internal server error"
        }
    }
)
def list_users(
    limit: int = Query(20, ge=1, le=100, description="Number of results per page"),
    offset: int = Query(0, ge=0, description="Number of results to skip"),
    db: Session = Depends(get_db),
) -> UserListResponse:
    """
    Retrieve all users with pagination.
    """
    try:
        service = UserService(db)
        return service.get_users(skip=offset, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail="An internal error occurred")


@router.get(
    "/users/{user_id}",
    response_model=UserResponse,
    summary="Get user by ID",
    description="Retrieve full information of a user by their ID.",
    tags=["users"],
    responses={
        200: {
            "description": "User retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "email": "user@example.com",
                        "full_name": "John Doe",
                        "created_at": "2024-01-10T08:00:00Z"
                    }
                }
            }
        },
        404: {
            "description": "User not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "User with ID 1 not found",
                        "code": "NOT_FOUND"
                    }
                }
            }
        },
        500: {
            "description": "Internal server error"
        }
    }
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
) -> UserResponse:
    """
    Retrieve full information of a user by ID.
    """
    try:
        service = UserService(db)
        return service.get_user(user_id)
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An internal error occurred")


@router.patch(
    "/users/{user_id}",
    response_model=UserResponse,
    summary="Update user",
    description="Update user email and/or full name. At least one field must be provided.",
    tags=["users"],
    responses={
        200: {
            "description": "User updated successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "email": "newemail@example.com",
                        "full_name": "Jane Doe",
                        "created_at": "2024-01-10T08:00:00Z"
                    }
                }
            }
        },
        400: {
            "description": "Validation error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid email format",
                        "code": "VALIDATION_ERROR"
                    }
                }
            }
        },
        404: {
            "description": "User not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "User with ID 1 not found",
                        "code": "NOT_FOUND"
                    }
                }
            }
        },
        409: {
            "description": "Email already exists",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Email newemail@example.com already exists",
                        "code": "DUPLICATE_EMAIL"
                    }
                }
            }
        }
    }
)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
) -> UserResponse:
    """
    Update user email and/or full name.
    """
    try:
        service = UserService(db)
        return service.update_user(user_id, user_update)
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except DuplicateEmailError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An internal error occurred")

