#!/usr/bin/env python
import os
import sys
import traceback

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=== Debugging Backend Startup ===")
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")

# Test 1: Import modules
print("\n1. Testing module imports...")
try:
    import flask
    print(f"✓ Flask imported: {flask.__version__}")
except Exception as e:
    print(f"✗ Flask import failed: {e}")

try:
    import flask_sqlalchemy
    print(f"✓ Flask-SQLAlchemy imported: {flask_sqlalchemy.__version__}")
except Exception as e:
    print(f"✗ Flask-SQLAlchemy import failed: {e}")

try:
    import flask_cors
    print(f"✓ Flask-CORS imported: {flask_cors.__version__}")
except Exception as e:
    print(f"✗ Flask-CORS import failed: {e}")

try:
    import flask_jwt_extended
    print(f"✓ Flask-JWT-Extended imported: {flask_jwt_extended.__version__}")
except Exception as e:
    print(f"✗ Flask-JWT-Extended import failed: {e}")

# Test 2: Import app module
print("\n2. Testing app module import...")
try:
    from app import create_app
    print("✓ app module imported")
except Exception as e:
    print(f"✗ app module import failed: {e}")
    traceback.print_exc()

# Test 3: Create app instance
print("\n3. Testing app creation...")
try:
    from app import create_app
    app = create_app('development')
    print("✓ App created successfully")
    print(f"App config: {app.config['ENV']}")
    print(f"Database URL: {app.config['SQLALCHEMY_DATABASE_URI']}")
except Exception as e:
    print(f"✗ App creation failed: {e}")
    traceback.print_exc()

# Test 4: Test database connection
print("\n4. Testing database connection...")
try:
    from app import create_app, db
    app = create_app('development')
    with app.app_context():
        db.create_all()
        print("✓ Database connection successful")
except Exception as e:
    print(f"✗ Database connection failed: {e}")
    traceback.print_exc()

print("\n=== Debugging Complete ===")
