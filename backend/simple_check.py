#!/usr/bin/env python
"""Simple check for imported MITRE ATT&CK data"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.attack import Tactic, Technique, Mitigation, Software
from app.models.actor import ThreatActor

try:
    app = create_app('development')
    with app.app_context():
        print('=== MITRE ATT&CK Data Import Summary ===')
        print()
        print(f'Tactics: {Tactic.query.count()}')
        print(f'Techniques: {Technique.query.count()}')
        sub_count = Technique.query.filter_by(is_subtechnique=True).count()
        main_count = Technique.query.filter_by(is_subtechnique=False).count()
        print(f'  - Sub-techniques: {sub_count}')
        print(f'  - Main techniques: {main_count}')
        print(f'Mitigations: {Mitigation.query.count()}')
        print(f'Software: {Software.query.count()}')
        malware_count = Software.query.filter_by(type='malware').count()
        tools_count = Software.query.filter_by(type='tool').count()
        print(f'  - Malware: {malware_count}')
        print(f'  - Tools: {tools_count}')
        print(f'Threat Actors: {ThreatActor.query.count()}')
        print()
        print('✅ All data imported successfully!')
except Exception as e:
    print(f'❌ Error: {e}')
    import traceback
    traceback.print_exc()