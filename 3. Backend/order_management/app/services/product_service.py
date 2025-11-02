"""
Product service for business logic operations.
"""
from typing import List, Tuple
from sqlalchemy.orm import Session
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse, ProductListResponse
from app.repositories.product_repository import ProductRepository
from app.utils.exceptions import ProductNotFoundError, ValidationError


class ProductService:
    """Product service with business logic."""
    
    def __init__(self, db: Session):
        """
        Initialize product service.
        
        Args:
            db: Database session
        """
        self.repository = ProductRepository(db)
        self.db = db
    
    def get_product(self, product_id: int) -> ProductResponse:
        """
        Get product by ID.
        
        Args:
            product_id: Product ID
            
        Returns:
            ProductResponse: Product response
            
        Raises:
            ProductNotFoundError: If product not found
        """
        product = self.repository.get(product_id)
        if not product:
            raise ProductNotFoundError(f"Product with ID {product_id} not found")
        return ProductResponse.model_validate(product)
    
    def get_products(
        self,
        skip: int = 0,
        limit: int = 20,
    ) -> ProductListResponse:
        """
        Get all products with pagination.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            ProductListResponse: List of products
        """
        products, total = self.repository.get_all(skip=skip, limit=limit)
        return ProductListResponse(
            items=[ProductResponse.model_validate(product) for product in products],
            total=total,
            limit=limit,
            offset=skip,
        )
    
    def create_product(self, product_data: ProductCreate) -> ProductResponse:
        """
        Create a new product.
        
        Args:
            product_data: Product creation data
            
        Returns:
            ProductResponse: Created product
            
        Raises:
            ValidationError: If validation fails
        """
        if product_data.price_cents < 0:
            raise ValidationError("Price must be non-negative")
        
        product = self.repository.create(product_data.model_dump())
        return ProductResponse.model_validate(product)
    
    def update_product(
        self,
        product_id: int,
        product_update: ProductUpdate,
    ) -> ProductResponse:
        """
        Update product information.
        
        Args:
            product_id: Product ID
            product_update: Product update data
            
        Returns:
            ProductResponse: Updated product
            
        Raises:
            ProductNotFoundError: If product not found
            ValidationError: If validation fails
        """
        # Check if product exists
        product = self.repository.get(product_id)
        if not product:
            raise ProductNotFoundError(f"Product with ID {product_id} not found")
        
        # Prepare update data
        update_data = {}
        
        if product_update.name is not None:
            if not product_update.name.strip():
                raise ValidationError("Product name cannot be empty")
            update_data["name"] = product_update.name
        
        if product_update.price_cents is not None:
            if product_update.price_cents < 0:
                raise ValidationError("Price must be non-negative")
            update_data["price_cents"] = product_update.price_cents
        
        if not update_data:
            raise ValidationError("At least one field must be provided for update")
        
        # Update product
        updated_product = self.repository.update(product_id, update_data)
        if not updated_product:
            raise ProductNotFoundError(f"Product with ID {product_id} not found")
        
        return ProductResponse.model_validate(updated_product)

