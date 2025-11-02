"""
FastAPI application entry point.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import orders, products, users

# Create FastAPI application
app = FastAPI(
    title="Order Management System API",
    description="Comprehensive REST API for managing orders, products, and users with full CRUD operations",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    tags_metadata=[
        {
            "name": "orders",
            "description": "Operations related to order management. Supports listing with multi-dimensional filtering, creation, and status updates.",
        },
        {
            "name": "products",
            "description": "Operations related to product catalog management. Create, list, and update products.",
        },
        {
            "name": "users",
            "description": "Operations related to user management. List and update user information.",
        },
    ],
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    orders.router,
    prefix=settings.API_V1_PREFIX,
    tags=["orders"],
)
app.include_router(
    products.router,
    prefix=settings.API_V1_PREFIX,
    tags=["products"],
)
app.include_router(
    users.router,
    prefix=settings.API_V1_PREFIX,
    tags=["users"],
)


@app.get("/", tags=["root"])
def root():
    """
    Root endpoint.
    
    Returns:
        dict: API information
    """
    return {
        "message": "Order Management System API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
    }


@app.get("/health", tags=["health"])
def health_check():
    """
    Health check endpoint.
    
    Returns:
        dict: Health status
    """
    return {"status": "healthy"}

