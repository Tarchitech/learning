"""
Product-related API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.services.product_service import ProductService
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse, ProductListResponse
from app.utils.exceptions import ProductNotFoundError, ValidationError

router = APIRouter()


@router.get(
    "/products",
    response_model=ProductListResponse,
    summary="List products",
    description="Retrieve a list of all products with pagination.",
    tags=["products"],
    responses={
        200: {
            "description": "Successful response with list of products",
            "content": {
                "application/json": {
                    "example": {
                        "items": [
                            {
                                "id": 1,
                                "name": "Product A",
                                "price_cents": 1999
                            }
                        ],
                        "total": 50,
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
def list_products(
    limit: int = Query(20, ge=1, le=100, description="Number of results per page"),
    offset: int = Query(0, ge=0, description="Number of results to skip"),
    db: Session = Depends(get_db),
) -> ProductListResponse:
    """
    Retrieve all products with pagination.
    """
    try:
        service = ProductService(db)
        return service.get_products(skip=offset, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail="An internal error occurred")


@router.get(
    "/products/{product_id}",
    response_model=ProductResponse,
    summary="Get product by ID",
    description="Retrieve full information of a product by its ID.",
    tags=["products"],
    responses={
        200: {
            "description": "Product retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "name": "Product A",
                        "price_cents": 1999
                    }
                }
            }
        },
        404: {
            "description": "Product not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Product with ID 1 not found",
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
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
) -> ProductResponse:
    """
    Retrieve full information of a product by ID.
    """
    try:
        service = ProductService(db)
        return service.get_product(product_id)
    except ProductNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An internal error occurred")


@router.post(
    "/products",
    response_model=ProductResponse,
    status_code=201,
    summary="Create product",
    description="Create a new product in the catalog.",
    tags=["products"],
    responses={
        201: {
            "description": "Product created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "name": "Product A",
                        "price_cents": 1999
                    }
                }
            }
        },
        400: {
            "description": "Validation error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Price must be non-negative",
                        "code": "VALIDATION_ERROR"
                    }
                }
            }
        }
    }
)
def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
) -> ProductResponse:
    """
    Create a new product.
    """
    try:
        service = ProductService(db)
        return service.create_product(product_data)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An internal error occurred")


@router.patch(
    "/products/{product_id}",
    response_model=ProductResponse,
    summary="Update product",
    description="Update product name and/or price. At least one field must be provided.",
    tags=["products"],
    responses={
        200: {
            "description": "Product updated successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "name": "Updated Product A",
                        "price_cents": 2499
                    }
                }
            }
        },
        400: {
            "description": "Validation error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "At least one field must be provided for update",
                        "code": "VALIDATION_ERROR"
                    }
                }
            }
        },
        404: {
            "description": "Product not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Product with ID 1 not found",
                        "code": "NOT_FOUND"
                    }
                }
            }
        }
    }
)
def update_product(
    product_id: int,
    product_update: ProductUpdate,
    db: Session = Depends(get_db),
) -> ProductResponse:
    """
    Update product name and/or price.
    """
    try:
        service = ProductService(db)
        return service.update_product(product_id, product_update)
    except ProductNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An internal error occurred")

