from app import db
from app.models.base import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash

# Association tables for many-to-many relationships
user_roles = db.Table('user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True)
)

role_permissions = db.Table('role_permissions',
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True),
    db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id'), primary_key=True)
)

class User(BaseModel):
    """User model"""
    __tablename__ = 'users'
    
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100))
    department = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime)
    login_count = db.Column(db.Integer, default=0)
    
    # Relationships
    roles = db.relationship('Role', secondary=user_roles, backref=db.backref('users', lazy='dynamic'))
    
    def set_password(self, password):
        """Set password hash"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password"""
        return check_password_hash(self.password_hash, password)
    
    def has_permission(self, permission_name):
        """Check if user has specific permission"""
        for role in self.roles:
            for permission in role.permissions:
                if permission.name == permission_name:
                    return True
        return self.is_admin
    
    def has_role(self, role_name):
        """Check if user has specific role"""
        return any(role.name == role_name for role in self.roles) or self.is_admin
    
    def get_permissions(self):
        """Get all user permissions"""
        permissions = set()
        for role in self.roles:
            for permission in role.permissions:
                permissions.add(permission.name)
        return list(permissions)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def to_dict(self):
        data = super().to_dict()
        data.pop('password_hash', None)
        data['roles'] = [role.name for role in self.roles]
        data['permissions'] = self.get_permissions()
        return data

class Role(BaseModel):
    """Role model"""
    __tablename__ = 'roles'
    
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255))
    is_system = db.Column(db.Boolean, default=False)  # System roles cannot be deleted
    
    # Relationships
    permissions = db.relationship('Permission', secondary=role_permissions, backref=db.backref('roles', lazy='dynamic'))
    
    def __repr__(self):
        return f'<Role {self.name}>'
    
    def to_dict(self):
        data = super().to_dict()
        data['permissions'] = [p.name for p in self.permissions]
        data['user_count'] = self.users.count()
        return data

class Permission(BaseModel):
    """Permission model"""
    __tablename__ = 'permissions'
    
    name = db.Column(db.String(80), unique=True, nullable=False)
    resource = db.Column(db.String(50), nullable=False)  # e.g., 'tactic', 'technique', 'rule'
    action = db.Column(db.String(50), nullable=False)  # e.g., 'view', 'create', 'edit', 'delete'
    description = db.Column(db.String(255))
    
    def __repr__(self):
        return f'<Permission {self.name}>'
    
    @staticmethod
    def create_permission_name(resource, action):
        """Create permission name from resource and action"""
        return f'{resource}:{action}'
