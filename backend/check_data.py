#!/usr/bin/env python
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Try to import and check
try:
    print('Checking database connection...')
    
    from app import create_app, db
    app = create_app('development')
    
    with app.app_context():
        print('Database connection successful!')
        
        # Check if tables exist
        from app.models.attack import Tactic, Technique
        
        # Count records
        tactic_count = Tactic.query.count()
        technique_count = Technique.query.count()
        
        print(f'Tactics: {tactic_count}')
        print(f'Techniques: {technique_count}')
        
        if tactic_count > 0 and technique_count > 0:
            print('SUCCESS: MITRE ATT&CK data is already imported!')
        else:
            print('WARNING: No data found in database.')
            
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()

print('Check completed.')