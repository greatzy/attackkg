#!/usr/bin/env python
import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print('=== Debug Initialization ===')

# Test 1: Import basic modules
print('\n1. Testing basic imports...')
try:
    import flask
    import sqlalchemy
    import flask_sqlalchemy
    import flask_cors
    import flask_jwt_extended
    print('   ✅ Basic imports successful')
except Exception as e:
    print(f'   ❌ Basic imports failed: {e}')

# Test 2: Import app module
print('\n2. Testing app import...')
try:
    from app import create_app
    print('   ✅ App module imported successfully')
except Exception as e:
    print(f'   ❌ App module import failed: {e}')
    import traceback
    traceback.print_exc()

# Test 3: Create app
print('\n3. Testing app creation...')
try:
    app = create_app('development')
    print('   ✅ App created successfully')
    print(f'   Debug mode: {app.debug}')
    print(f'   Config: {app.config.__class__.__name__}')
except Exception as e:
    print(f'   ❌ App creation failed: {e}')
    import traceback
    traceback.print_exc()

# Test 4: Test database connection
print('\n4. Testing database connection...')
try:
    from app import db
    with app.app_context():
        # Test database connection
        db.session.execute('SELECT 1')
        print('   ✅ Database connection successful')
except Exception as e:
    print(f'   ❌ Database connection failed: {e}')
    import traceback
    traceback.print_exc()

# Test 5: Test ATT&CK data
print('\n5. Testing ATT&CK data...')
try:
    from app.models.attack import Tactic, Technique
    with app.app_context():
        tactic_count = Tactic.query.count()
        technique_count = Technique.query.count()
        print(f'   ✅ ATT&CK data found: {tactic_count} tactics, {technique_count} techniques')
except Exception as e:
    print(f'   ❌ ATT&CK data test failed: {e}')
    import traceback
    traceback.print_exc()

print('\n=== Debug Complete ===')