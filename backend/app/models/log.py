from app import db
from app.models.base import BaseModel

class OperationLog(BaseModel):
    """Operation audit log"""
    __tablename__ = 'operation_logs'
    
    # User info
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    username = db.Column(db.String(80))
    ip_address = db.Column(db.String(45))  # IPv6 compatible
    user_agent = db.Column(db.String(500))
    
    # Operation info
    action = db.Column(db.String(50), nullable=False)  # create, update, delete, view, login, logout, etc.
    resource_type = db.Column(db.String(50))  # tactic, technique, actor, rule, etc.
    resource_id = db.Column(db.String(100))
    resource_name = db.Column(db.String(200))
    
    # Request details
    method = db.Column(db.String(10))  # GET, POST, PUT, DELETE
    path = db.Column(db.String(500))
    request_data = db.Column(db.JSON)
    response_status = db.Column(db.Integer)
    
    # Additional info
    description = db.Column(db.Text)
    result = db.Column(db.String(20))  # success, failure
    error_message = db.Column(db.Text)
    duration = db.Column(db.Integer)  # Request duration in milliseconds
    
    # Relationships
    user = db.relationship('User', backref='operation_logs')
    
    def __repr__(self):
        return f'<OperationLog {self.id}: {self.action} {self.resource_type}>'
    
    def to_dict(self):
        data = super().to_dict()
        data.pop('request_data', None)  # Remove sensitive data
        return data
