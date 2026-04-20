#!/usr/bin/env python
import sys
import os
import traceback

print("Python version:", sys.version_info)
print("System path:", sys.path)
print("Current directory:", os.getcwd())

try:
    print("\n=== Importing app module ===")
    import app
    print("App module imported successfully")
    print(f"App module: {app}")
    print(f"App module attributes: {dir(app)}")
    
    print("\n=== Creating app instance ===")
    from app import create_app
    app = create_app('development')
    print("App instance created successfully")
    print(f"App instance: {app}")
    
except Exception as e:
    print(f"\nError: {str(e)}")
    print(f"Type: {type(e)}")
    print("Traceback:")
    print(traceback.format_exc())
    
print("\n=== System check completed ===")
