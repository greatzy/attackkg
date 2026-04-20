#!/usr/bin/env python
"""Verify matrix data is complete"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.attack import Tactic, Technique

app = create_app('development')
with app.app_context():
    print("=== ATT&CK Matrix Data Verification ===")
    print()
    
    tactics = Tactic.query.all()
    print(f"Total Tactics: {len(tactics)}")
    print()
    
    total_techniques = 0
    for tactic in tactics:
        count = Technique.query.filter_by(tactic_id=tactic.tactic_id).count()
        total_techniques += count
        print(f"{tactic.tactic_id}: {tactic.name} - {count} techniques")
    
    print()
    print(f"Total techniques in matrix: {total_techniques}")
    print(f"Expected: 691")
    print()
    
    if total_techniques == 691:
        print("✅ All techniques are correctly mapped to tactics!")
    else:
        print(f"⚠️  Missing {691 - total_techniques} techniques")
