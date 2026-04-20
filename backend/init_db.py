#!/usr/bin/env python
"""
Database initialization script for AttackKG system
Creates all necessary tables and initializes with default data
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.user import User, Role, Permission
from app.models.log import OperationLog
from app.models.attack import Tactic, Technique
from app.models.actor import ThreatActor
from app.models.rule import DetectionRule
from app.models.intelligence import ThreatIntelligence
from app.models.report import Report
from werkzeug.security import generate_password_hash

def init_database():
    """Initialize the database with all tables and initial data"""
    
    print("Initializing AttackKG database...")
    
    try:
        # Create app with test configuration
        app = create_app('development')
        
        with app.app_context():
            # Create all tables
            print("Creating database tables...")
            db.create_all()
            print("Tables created successfully")
            
            # Create initial permissions
            print("Creating initial permissions...")
            permissions = [
                Permission(name='view_attack_data', resource='attack', action='view', description='View ATT&CK data'),
                Permission(name='manage_attack_data', resource='attack', action='manage', description='Manage ATT&CK data'),
                Permission(name='view_actors', resource='actors', action='view', description='View threat actors'),
                Permission(name='manage_actors', resource='actors', action='manage', description='Manage threat actors'),
                Permission(name='view_rules', resource='rules', action='view', description='View detection rules'),
                Permission(name='manage_rules', resource='rules', action='manage', description='Manage detection rules'),
                Permission(name='view_intelligence', resource='intelligence', action='view', description='View threat intelligence'),
                Permission(name='manage_intelligence', resource='intelligence', action='manage', description='Manage threat intelligence'),
                Permission(name='view_reports', resource='reports', action='view', description='View reports'),
                Permission(name='manage_reports', resource='reports', action='manage', description='Manage reports'),
                Permission(name='view_system', resource='system', action='view', description='View system settings'),
                Permission(name='manage_system', resource='system', action='manage', description='Manage system settings'),
                Permission(name='manage_users', resource='users', action='manage', description='Manage users and permissions'),
            ]
            
            for perm in permissions:
                existing = Permission.query.filter_by(name=perm.name).first()
                if not existing:
                    db.session.add(perm)
            
            # Create initial roles
            print("Creating initial roles...")
            roles = [
                Role(
                    name='admin',
                    description='System administrator with all permissions'
                ),
                Role(
                    name='analyst',
                    description='Security analyst with access to analysis features'
                ),
                Role(
                    name='user',
                    description='Regular user with basic access'
                )
            ]
            
            for role in roles:
                existing = Role.query.filter_by(name=role.name).first()
                if not existing:
                    db.session.add(role)
            
            db.session.commit()
            
            # Assign permissions to roles
            print("Assigning permissions to roles...")
            admin_role = Role.query.filter_by(name='admin').first()
            if admin_role:
                admin_role.permissions = Permission.query.all()
            
            analyst_role = Role.query.filter_by(name='analyst').first()
            if analyst_role:
                analyst_role.permissions = Permission.query.filter(
                    Permission.name.in_([
                        'view_attack_data', 'view_actors', 'view_rules',
                        'view_intelligence', 'view_reports'
                    ])
                ).all()
            
            user_role = Role.query.filter_by(name='user').first()
            if user_role:
                user_role.permissions = Permission.query.filter(
                    Permission.name.in_([
                        'view_attack_data', 'view_actors', 'view_intelligence', 'view_reports'
                    ])
                ).all()
            
            # Create default admin user
            print("Creating default admin user...")
            admin_user = User.query.filter_by(username='admin').first()
            if not admin_user:
                admin_user = User(
                    username='admin',
                    email='admin@attackkg.com',
                    password_hash=generate_password_hash('admin123'),
                    is_admin=True,
                    is_active=True
                )
                admin_user.roles.append(admin_role)
                db.session.add(admin_user)
            
            # Create test user
            print("Creating test user...")
            test_user = User.query.filter_by(username='testuser').first()
            if not test_user:
                test_user = User(
                    username='testuser',
                    email='test@example.com',
                    password_hash=generate_password_hash('testpassword'),
                    is_active=True
                )
                test_user.roles.append(analyst_role)
                db.session.add(test_user)
            
            db.session.commit()
            
            print("Database initialized successfully!")
            print()
            print("Default users created:")
            print("  - Username: admin, Password: admin123 (Admin user)")
            print("  - Username: testuser, Password: testpassword (Test user)")
            
            return True
            
    except Exception as e:
        print(f"Error initializing database: {e}")
        import traceback
        print(f"Detailed error: {traceback.format_exc()}")
        return False

def drop_database():
    """Drops all tables from the database"""
    try:
        app = create_app('development')
        with app.app_context():
            db.drop_all()
            print("Database tables dropped successfully")
            return True
    except Exception as e:
        print(f"Error dropping database: {e}")
        return False

def reset_database():
    """Resets the database by dropping and recreating all tables"""
    print("Resetting database...")
    if drop_database():
        return init_database()
    return False

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'reset':
        reset_database()
    elif len(sys.argv) > 1 and sys.argv[1] == 'drop':
        drop_database()
    else:
        init_database()
