#!/usr/bin/env python
import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import create_app
    print("Creating app...")
    app = create_app('development')
    
    print("App created successfully!")
    print(f"Debug mode: {app.debug}")
    print(f"Config class: {app.config.__class__.__name__}")
    print(f"Database URL: {app.config.get('SQLALCHEMY_DATABASE_URI')}")
    
    print("\nAttempting to start server...")
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
    
except Exception as e:
    print(f"\nError: {str(e)}")
    print("\nTraceback:")
    import traceback
    print(traceback.format_exc())
    sys.exit(1)
