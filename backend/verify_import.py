#!/usr/bin/env python
"""Verify MITRE ATT&CK data import"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.attack import Tactic, Technique, Mitigation, Software
from app.models.actor import ThreatActor

try:
    print('=== Verifying MITRE ATT&CK Data Import ===')
    print()
    
    app = create_app('development')
    
    with app.app_context():
        print('Database connected successfully!')
        print()
        
        # Count data
        tactic_count = Tactic.query.count()
        technique_count = Technique.query.count()
        mitigation_count = Mitigation.query.count()
        software_count = Software.query.count()
        actor_count = ThreatActor.query.count()
        
        print(f'Tactics: {tactic_count}')
        print(f'Techniques: {technique_count}')
        print(f'Mitigations: {mitigation_count}')
        print(f'Software: {software_count}')
        print(f'Threat Actors: {actor_count}')
        print()
        
        # Check if data exists
        if tactic_count > 0 and technique_count > 0:
            print('✅ Data import verification PASSED!')
            print('   MITRE ATT&CK data has been successfully imported.')
        else:
            print('❌ Data import verification FAILED!')
            print('   No data found in the database.')
            
        print()
        print('=== Verification Complete ===')
        
except Exception as e:
    print(f'❌ Error during verification: {e}')
    import traceback
    traceback.print_exc()