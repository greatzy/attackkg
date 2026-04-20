#!/usr/bin/env python
"""
Import MITRE ATT&CK data from local JSON file
Usage: Place the downloaded enterprise-attack-18.1.json file in the same directory and run this script
"""

import sys
import os
import json
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.attack import Tactic, Technique, Mitigation, Software
from app.models.actor import ThreatActor

# Local file path
LOCAL_FILE = 'enterprise-attack-18.1.json'

def load_local_data():
    """Load ATT&CK data from local file"""
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), LOCAL_FILE)
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        print(f"\nPlease download the file from:")
        print(f"https://github.com/mitre-attack/attack-stix-data/blob/master/enterprise-attack/enterprise-attack-18.1.json")
        print(f"\nAnd place it in: {os.path.dirname(os.path.abspath(__file__))}")
        return None
    
    print(f"Loading data from {file_path}...")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        file_size = os.path.getsize(file_path) / 1024 / 1024
        print(f"✅ Loaded {file_size:.2f} MB")
        return data
    except Exception as e:
        print(f"❌ Failed to load file: {e}")
        return None

def parse_stix_data(data):
    """Parse STIX data and extract objects"""
    objects = data.get('objects', [])
    print(f"Total objects in STIX bundle: {len(objects)}")
    
    # Categorize objects by type
    tactics = []
    techniques = []
    mitigations = []
    malware = []
    tools = []
    actors = []
    relationships = []
    
    for obj in objects:
        obj_type = obj.get('type')
        
        if obj_type == 'x-mitre-tactic':
            tactics.append(obj)
        elif obj_type == 'attack-pattern':
            # Skip deprecated and revoked
            if not obj.get('x_mitre_deprecated') and not obj.get('revoked'):
                techniques.append(obj)
        elif obj_type == 'course-of-action':
            mitigations.append(obj)
        elif obj_type == 'malware':
            malware.append(obj)
        elif obj_type == 'tool':
            tools.append(obj)
        elif obj_type == 'intrusion-set':
            actors.append(obj)
        elif obj_type == 'relationship':
            relationships.append(obj)
    
    print(f"Found:")
    print(f"  - {len(tactics)} tactics")
    print(f"  - {len(techniques)} techniques")
    print(f"  - {len(mitigations)} mitigations")
    print(f"  - {len(malware)} malware")
    print(f"  - {len(tools)} tools")
    print(f"  - {len(actors)} actors")
    print(f"  - {len(relationships)} relationships")
    
    return {
        'tactics': tactics,
        'techniques': techniques,
        'mitigations': mitigations,
        'malware': malware,
        'tools': tools,
        'actors': actors,
        'relationships': relationships
    }

def get_mitre_id(obj):
    """Extract MITRE ATT&CK ID from external references"""
    external_refs = obj.get('external_references', [])
    for ref in external_refs:
        if ref.get('source_name') == 'mitre-attack':
            return ref.get('external_id')
    return None

def get_url(obj):
    """Extract URL from external references"""
    external_refs = obj.get('external_references', [])
    for ref in external_refs:
        if ref.get('source_name') == 'mitre-attack':
            return ref.get('url', '')
    return ''

def import_tactics(app, tactics):
    """Import tactics to database"""
    print("\nImporting tactics...")
    
    with app.app_context():
        count = 0
        for tactic_data in tactics:
            tactic_id = get_mitre_id(tactic_data)
            if not tactic_id:
                continue
            
            existing = Tactic.query.filter_by(tactic_id=tactic_id).first()
            if existing:
                existing.name = tactic_data.get('name', '')
                existing.description = tactic_data.get('description', '')
                existing.url = get_url(tactic_data)
                existing.updated_at = datetime.now()
            else:
                tactic = Tactic(
                    tactic_id=tactic_id,
                    name=tactic_data.get('name', ''),
                    description=tactic_data.get('description', ''),
                    url=get_url(tactic_data),
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                db.session.add(tactic)
                count += 1
        
        db.session.commit()
        print(f"✅ Imported/Updated {len(tactics)} tactics ({count} new)")

def import_techniques(app, techniques):
    """Import techniques to database"""
    print("\nImporting techniques...")
    
    with app.app_context():
        count = 0
        for tech_data in techniques:
            technique_id = get_mitre_id(tech_data)
            if not technique_id:
                continue
            
            is_subtechnique = '.' in technique_id
            platforms = tech_data.get('x_mitre_platforms', [])
            
            # Get tactic ID from kill chain phases
            tactic_id = None
            kill_chain_phases = tech_data.get('kill_chain_phases', [])
            for phase in kill_chain_phases:
                if phase.get('kill_chain_name') == 'mitre-attack':
                    phase_name = phase.get('phase_name', '')
                    break
            
            existing = Technique.query.filter_by(technique_id=technique_id).first()
            if existing:
                existing.name = tech_data.get('name', '')
                existing.description = tech_data.get('description', '')
                existing.url = get_url(tech_data)
                existing.platforms = platforms
                existing.is_subtechnique = is_subtechnique
                existing.updated_at = datetime.now()
            else:
                technique = Technique(
                    technique_id=technique_id,
                    name=tech_data.get('name', ''),
                    description=tech_data.get('description', ''),
                    url=get_url(tech_data),
                    platforms=platforms,
                    is_subtechnique=is_subtechnique,
                    tactic_id=tactic_id,
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                db.session.add(technique)
                count += 1
        
        db.session.commit()
        print(f"✅ Imported/Updated {len(techniques)} techniques ({count} new)")

def import_mitigations(app, mitigations):
    """Import mitigations to database"""
    print("\nImporting mitigations...")
    
    with app.app_context():
        count = 0
        for mit_data in mitigations:
            mitigation_id = get_mitre_id(mit_data)
            if not mitigation_id:
                continue
            
            existing = Mitigation.query.filter_by(mitigation_id=mitigation_id).first()
            if existing:
                existing.name = mit_data.get('name', '')
                existing.description = mit_data.get('description', '')
                existing.url = get_url(mit_data)
                existing.updated_at = datetime.now()
            else:
                mitigation = Mitigation(
                    mitigation_id=mitigation_id,
                    name=mit_data.get('name', ''),
                    description=mit_data.get('description', ''),
                    url=get_url(mit_data),
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                db.session.add(mitigation)
                count += 1
        
        db.session.commit()
        print(f"✅ Imported/Updated {len(mitigations)} mitigations ({count} new)")

def import_software(app, malware, tools):
    """Import software (malware and tools) to database"""
    print("\nImporting software...")
    
    with app.app_context():
        count = 0
        
        for mal_data in malware:
            software_id = get_mitre_id(mal_data)
            if not software_id:
                continue
            
            existing = Software.query.filter_by(software_id=software_id).first()
            if existing:
                existing.name = mal_data.get('name', '')
                existing.description = mal_data.get('description', '')
                existing.type = 'malware'
                existing.url = get_url(mal_data)
                existing.updated_at = datetime.now()
            else:
                software = Software(
                    software_id=software_id,
                    name=mal_data.get('name', ''),
                    description=mal_data.get('description', ''),
                    type='malware',
                    url=get_url(mal_data),
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                db.session.add(software)
                count += 1
        
        for tool_data in tools:
            software_id = get_mitre_id(tool_data)
            if not software_id:
                continue
            
            existing = Software.query.filter_by(software_id=software_id).first()
            if existing:
                existing.name = tool_data.get('name', '')
                existing.description = tool_data.get('description', '')
                existing.type = 'tool'
                existing.url = get_url(tool_data)
                existing.updated_at = datetime.now()
            else:
                software = Software(
                    software_id=software_id,
                    name=tool_data.get('name', ''),
                    description=tool_data.get('description', ''),
                    type='tool',
                    url=get_url(tool_data),
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                db.session.add(software)
                count += 1
        
        db.session.commit()
        total = len(malware) + len(tools)
        print(f"✅ Imported/Updated {total} software ({count} new)")

def import_actors(app, actors):
    """Import threat actors to database"""
    print("\nImporting threat actors...")
    
    with app.app_context():
        count = 0
        for actor_data in actors:
            actor_id = get_mitre_id(actor_data)
            if not actor_id:
                continue
            
            existing = ThreatActor.query.filter_by(actor_id=actor_id).first()
            if existing:
                existing.name = actor_data.get('name', '')
                existing.description = actor_data.get('description', '')
                existing.url = get_url(actor_data)
                existing.updated_at = datetime.now()
            else:
                actor = ThreatActor(
                    actor_id=actor_id,
                    name=actor_data.get('name', ''),
                    description=actor_data.get('description', ''),
                    url=get_url(actor_data),
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                db.session.add(actor)
                count += 1
        
        db.session.commit()
        print(f"✅ Imported/Updated {len(actors)} actors ({count} new)")

def main():
    print("=" * 70)
    print("MITRE ATT&CK Enterprise v18.1 Data Importer (Local File)")
    print("=" * 70)
    
    app = create_app('development')
    
    # Load local data
    data = load_local_data()
    if not data:
        print("\n❌ Failed to load data. Exiting.")
        return
    
    # Parse STIX data
    print("\nParsing STIX data...")
    parsed_data = parse_stix_data(data)
    
    # Import to database
    print("\n" + "=" * 70)
    print("Importing data to database...")
    print("=" * 70)
    
    import_tactics(app, parsed_data['tactics'])
    import_techniques(app, parsed_data['techniques'])
    import_mitigations(app, parsed_data['mitigations'])
    import_software(app, parsed_data['malware'], parsed_data['tools'])
    import_actors(app, parsed_data['actors'])
    
    print("\n" + "=" * 70)
    print("✅ Import completed successfully!")
    print("=" * 70)

if __name__ == '__main__':
    main()
