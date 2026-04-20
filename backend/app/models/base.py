from datetime import datetime
from app import db

class BaseModel(db.Model):
    """Base model with common attributes and methods"""
    __abstract__ = True
    
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def save(self):
        """Save model instance"""
        db.session.add(self)
        db.session.commit()
        return self
    
    def delete(self):
        """Delete model instance"""
        db.session.delete(self)
        db.session.commit()
    
    def update(self, **kwargs):
        """Update model attributes"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.utcnow()
        db.session.commit()
        return self
    
    @classmethod
    def get_by_id(cls, id):
        """Get instance by ID"""
        return cls.query.get(id)
    
    @classmethod
    def get_all(cls):
        """Get all instances"""
        return cls.query.all()
    
    @classmethod
    def get_paginated(cls, page=1, per_page=20, **filters):
        """Get paginated instances"""
        query = cls.query
        
        # Apply filters
        for key, value in filters.items():
            if value is not None and hasattr(cls, key):
                query = query.filter(getattr(cls, key) == value)
        
        return query.paginate(page=page, per_page=per_page, error_out=False)
    
    def to_dict(self, include_counts=False, **kwargs):
        """Convert model to dictionary"""
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if isinstance(value, datetime):
                result[column.name] = value.isoformat()
            else:
                result[column.name] = value
        return result
    
    def __repr__(self):
        return f'<{self.__class__.__name__} {self.id}>'
