"""
Base repository with common CRUD operations.
"""
from typing import Generic, TypeVar, Type, Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Base repository class with common CRUD operations."""
    
    def __init__(self, model: Type[ModelType], db: Session):
        """
        Initialize repository.
        
        Args:
            model: SQLAlchemy model class
            db: Database session
        """
        self.model = model
        self.db = db
    
    def get(self, id: int) -> Optional[ModelType]:
        """
        Get entity by ID.
        
        Args:
            id: Entity ID
            
        Returns:
            Optional[ModelType]: Entity or None if not found
        """
        return self.db.query(self.model).filter(self.model.id == id).first()
    
    def get_all(
        self,
        skip: int = 0,
        limit: int = 20,
    ) -> tuple[List[ModelType], int]:
        """
        Get all entities with pagination.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            tuple: (list of entities, total count)
        """
        query = self.db.query(self.model)
        total = query.count()
        items = query.offset(skip).limit(limit).all()
        return items, total
    
    def create(self, obj_data: dict) -> ModelType:
        """
        Create a new entity.
        
        Args:
            obj_data: Dictionary with entity data
            
        Returns:
            ModelType: Created entity
        """
        db_obj = self.model(**obj_data)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
    
    def update(self, id: int, obj_data: dict) -> Optional[ModelType]:
        """
        Update an entity.
        
        Args:
            id: Entity ID
            obj_data: Dictionary with updated data
            
        Returns:
            Optional[ModelType]: Updated entity or None if not found
        """
        db_obj = self.get(id)
        if not db_obj:
            return None
        
        for key, value in obj_data.items():
            setattr(db_obj, key, value)
        
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
    
    def delete(self, id: int) -> bool:
        """
        Delete an entity.
        
        Args:
            id: Entity ID
            
        Returns:
            bool: True if deleted, False if not found
        """
        db_obj = self.get(id)
        if not db_obj:
            return False
        
        self.db.delete(db_obj)
        self.db.commit()
        return True

