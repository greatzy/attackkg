#!/usr/bin/env python
"""
Fix tactic-technique relationships in the database
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.attack import Tactic, Technique

def fix_relations():
    """Fix tactic-technique relationships using the downloaded STIX data"""
    
    # Load the STIX data file
    stix_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'enterprise-attack-18.1.json')
    
    if not os.path.exists(stix_file):
        print(f"❌ STIX file not found: {stix_file}")
        return
    
    print("Loading STIX data...")
    with open(stix_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    objects = {obj['id']: obj for obj in data.get('objects', [])}
    
    # Build tactic ID mapping
    tactic_mapping = {}  # tactic STIX ID -> tactic MITRE ID
    for obj in objects.values():
        if obj.get('type') == 'x-mitre-tactic':
            external_refs = obj.get('external_references', [])
            for ref in external_refs:
                if ref.get('source_name') == 'mitre-attack':
                    tactic_mapping[obj['id']] = ref.get('external_id')
                    break
    
    print(f"Found {len(tactic_mapping)} tactics in STIX data")
    
    # Build technique-tactic relationships from kill chain phases
    technique_tactics = {}  # technique MITRE ID -> list of tactic MITRE IDs
    
    for obj in objects.values():
        if obj.get('type') == 'attack-pattern':
            # Skip deprecated and revoked
            if obj.get('x_mitre_deprecated') or obj.get('revoked'):
                continue
            
            # Get technique MITRE ID
            external_refs = obj.get('external_references', [])
            technique_id = None
            for ref in external_refs:
                if ref.get('source_name') == 'mitre-attack':
                    technique_id = ref.get('external_id')
                    break
            
            if not technique_id:
                continue
            
            # Get tactics from kill chain phases
            kill_chain_phases = obj.get('kill_chain_phases', [])
            tactics = []
            for phase in kill_chain_phases:
                if phase.get('kill_chain_name') == 'mitre-attack':
                    phase_name = phase.get('phase_name', '')
                    # Map phase name to tactic ID
                    # Phase names are like "initial-access", we need to find the corresponding tactic
                    for tactic_obj in objects.values():
                        if tactic_obj.get('type') == 'x-mitre-tactic':
                            if tactic_obj.get('x_mitre_shortname') == phase_name:
                                external_refs = tactic_obj.get('external_references', [])
                                for ref in external_refs:
                                    if ref.get('source_name') == 'mitre-attack':
                                        tactic_id = ref.get('external_id')
                                        if tactic_id:
                                            tactics.append(tactic_id)
                                        break
                                break
            
            if tactics:
                technique_tactics[technique_id] = tactics
    
    print(f"Found {len(technique_tactics)} techniques with tactic relationships")
    
    # Update database
    app = create_app('development')
    with app.app_context():
        updated_count = 0
        
        for technique_id, tactic_ids in technique_tactics.items():
            technique = Technique.query.filter_by(technique_id=technique_id).first()
            if technique:
                # Use the first tactic as the primary tactic
                primary_tactic_id = tactic_ids[0]
                technique.tactic_id = primary_tactic_id
                updated_count += 1
                
                if updated_count % 100 == 0:
                    print(f"  Updated {updated_count} techniques...")
        
        db.session.commit()
        print(f"✅ Updated {updated_count} techniques with tactic relationships")
        
        # Verify the fix
        print("\nVerifying fix...")
        techniques_with_tactic = Technique.query.filter(Technique.tactic_id.isnot(None)).count()
        print(f"Techniques with tactic_id: {techniques_with_tactic}")
        print(f"Total techniques: {Technique.query.count()}")

if __name__ == '__main__':
    print("=" * 70)
    print("Fixing Tactic-Technique Relationships")
    print("=" * 70)
    fix_relations()
    print("\n✅ Done!")
