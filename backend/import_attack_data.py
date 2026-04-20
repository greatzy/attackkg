#!/usr/bin/env python
"""
Import MITRE ATT&CK data from STIX format
Data source: https://github.com/mitre-attack/attack-stix-data
"""

import sys
import os
import json
import requests
from datetime import datetime
from typing import Dict, List, Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.attack import Tactic, Technique, SubTechnique, Mitigation, Software
from app.models.actor import ThreatActor

# MITRE ATT&CK STIX 2.1 data URLs
ATTACK_DATA_URLS = {
    'enterprise': 'https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack.json',
    'mobile': 'https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/mobile-attack/mobile-attack.json',
    'ics': 'https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/ics-attack/ics-attack.json'
}

class AttackDataImporter:
    def __init__(self, app):
        self.app = app
        self.objects = {}
        
    def fetch_data(self, domain='enterprise'):
        """Fetch ATT&CK data from GitHub"""
        url = ATTACK_DATA_URLS.get(domain)
        if not url:
            raise ValueError(f"Unknown domain: {domain}")
        
        print(f"Fetching ATT&CK data from {url}...")
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        
        data = response.json()
        self.objects = {obj['id']: obj for obj in data.get('objects', [])}
        return data
    
    def get_object_by_id(self, obj_id):
        """Get object by STIX ID"""
        return self.objects.get(obj_id)
    
    def get_objects_by_type(self, obj_type):
        """Get all objects of a specific type"""
        return [obj for obj in self.objects.values() if obj.get('type') == obj_type]
    
    def import_tactics(self):
        """Import tactics (x-mitre-tactic)"""
        print("Importing tactics...")
        tactics = self.get_objects_by_type('x-mitre-tactic')
        
        with self.app.app_context():
            for tactic_data in tactics:
                external_refs = tactic_data.get('external_references', [])
                tactic_id = None
                for ref in external_refs:
                    if ref.get('source_name') == 'mitre-attack':
                        tactic_id = ref.get('external_id')
                        break
                
                if not tactic_id:
                    continue
                
                # Check if tactic already exists
                existing = Tactic.query.filter_by(tactic_id=tactic_id).first()
                if existing:
                    print(f"  Tactic {tactic_id} already exists, updating...")
                    existing.name = tactic_data.get('name', '')
                    existing.description = tactic_data.get('description', '')
                    existing.url = tactic_data.get('external_references', [{}])[0].get('url', '')
                else:
                    print(f"  Creating tactic {tactic_id}...")
                    tactic = Tactic(
                        tactic_id=tactic_id,
                        name=tactic_data.get('name', ''),
                        description=tactic_data.get('description', ''),
                        url=tactic_data.get('external_references', [{}])[0].get('url', ''),
                        created_at=datetime.now(),
                        updated_at=datetime.now()
                    )
                    db.session.add(tactic)
            
            db.session.commit()
            print(f"Imported {len(tactics)} tactics")
    
    def import_techniques(self):
        """Import techniques (attack-pattern)"""
        print("Importing techniques...")
        techniques = self.get_objects_by_type('attack-pattern')
        
        with self.app.app_context():
            for tech_data in techniques:
                # Skip deprecated and revoked
                if tech_data.get('x_mitre_deprecated') or tech_data.get('revoked'):
                    continue
                
                external_refs = tech_data.get('external_references', [])
                technique_id = None
                for ref in external_refs:
                    if ref.get('source_name') == 'mitre-attack':
                        technique_id = ref.get('external_id')
                        break
                
                if not technique_id:
                    continue
                
                # Determine if it's a sub-technique
                is_subtechnique = '.' in technique_id
                
                # Get platforms
                platforms = tech_data.get('x_mitre_platforms', [])
                
                # Get tactic relationships
                tactic_ids = []
                for rel in self.get_objects_by_type('relationship'):
                    if (rel.get('relationship_type') == 'uses' and 
                        rel.get('source_ref') == tech_data['id']):
                        target = self.get_object_by_id(rel.get('target_ref', ''))
                        if target and target.get('type') == 'x-mitre-tactic':
                            for ref in target.get('external_references', []):
                                if ref.get('source_name') == 'mitre-attack':
                                    tactic_ids.append(ref.get('external_id'))
                                    break
                
                # Check if technique already exists
                existing = Technique.query.filter_by(technique_id=technique_id).first()
                if existing:
                    print(f"  Technique {technique_id} already exists, updating...")
                    existing.name = tech_data.get('name', '')
                    existing.description = tech_data.get('description', '')
                    existing.url = tech_data.get('external_references', [{}])[0].get('url', '')
                    existing.platforms = platforms
                    existing.is_subtechnique = is_subtechnique
                    if tactic_ids:
                        existing.tactic_id = tactic_ids[0]
                else:
                    print(f"  Creating technique {technique_id}...")
                    technique = Technique(
                        technique_id=technique_id,
                        name=tech_data.get('name', ''),
                        description=tech_data.get('description', ''),
                        url=tech_data.get('external_references', [{}])[0].get('url', ''),
                        platforms=platforms,
                        is_subtechnique=is_subtechnique,
                        tactic_id=tactic_ids[0] if tactic_ids else None,
                        created_at=datetime.now(),
                        updated_at=datetime.now()
                    )
                    db.session.add(technique)
            
            db.session.commit()
            print(f"Imported {len(techniques)} techniques")
    
    def import_mitigations(self):
        """Import mitigations (course-of-action)"""
        print("Importing mitigations...")
        mitigations = self.get_objects_by_type('course-of-action')
        
        with self.app.app_context():
            for mit_data in mitigations:
                external_refs = mit_data.get('external_references', [])
                mitigation_id = None
                for ref in external_refs:
                    if ref.get('source_name') == 'mitre-attack':
                        mitigation_id = ref.get('external_id')
                        break
                
                if not mitigation_id:
                    continue
                
                # Check if mitigation already exists
                existing = Mitigation.query.filter_by(mitigation_id=mitigation_id).first()
                if existing:
                    print(f"  Mitigation {mitigation_id} already exists, updating...")
                    existing.name = mit_data.get('name', '')
                    existing.description = mit_data.get('description', '')
                    existing.url = mit_data.get('external_references', [{}])[0].get('url', '')
                else:
                    print(f"  Creating mitigation {mitigation_id}...")
                    mitigation = Mitigation(
                        mitigation_id=mitigation_id,
                        name=mit_data.get('name', ''),
                        description=mit_data.get('description', ''),
                        url=mit_data.get('external_references', [{}])[0].get('url', ''),
                        created_at=datetime.now(),
                        updated_at=datetime.now()
                    )
                    db.session.add(mitigation)
            
            db.session.commit()
            print(f"Imported {len(mitigations)} mitigations")
    
    def import_software(self):
        """Import software (malware and tools)"""
        print("Importing software...")
        software_list = []
        
        # Malware
        malware_list = self.get_objects_by_type('malware')
        for mal_data in malware_list:
            external_refs = mal_data.get('external_references', [])
            software_id = None
            for ref in external_refs:
                if ref.get('source_name') == 'mitre-attack':
                    software_id = ref.get('external_id')
                    break
            
            if software_id:
                software_list.append({
                    'software_id': software_id,
                    'name': mal_data.get('name', ''),
                    'description': mal_data.get('description', ''),
                    'type': 'malware',
                    'url': mal_data.get('external_references', [{}])[0].get('url', '')
                })
        
        # Tools
        tools = self.get_objects_by_type('tool')
        for tool_data in tools:
            external_refs = tool_data.get('external_references', [])
            software_id = None
            for ref in external_refs:
                if ref.get('source_name') == 'mitre-attack':
                    software_id = ref.get('external_id')
                    break
            
            if software_id:
                software_list.append({
                    'software_id': software_id,
                    'name': tool_data.get('name', ''),
                    'description': tool_data.get('description', ''),
                    'type': 'tool',
                    'url': tool_data.get('external_references', [{}])[0].get('url', '')
                })
        
        with self.app.app_context():
            for sw_data in software_list:
                existing = Software.query.filter_by(software_id=sw_data['software_id']).first()
                if existing:
                    print(f"  Software {sw_data['software_id']} already exists, updating...")
                    existing.name = sw_data['name']
                    existing.description = sw_data['description']
                    existing.type = sw_data['type']
                    existing.url = sw_data['url']
                else:
                    print(f"  Creating software {sw_data['software_id']}...")
                    software = Software(
                        software_id=sw_data['software_id'],
                        name=sw_data['name'],
                        description=sw_data['description'],
                        type=sw_data['type'],
                        url=sw_data['url'],
                        created_at=datetime.now(),
                        updated_at=datetime.now()
                    )
                    db.session.add(software)
            
            db.session.commit()
            print(f"Imported {len(software_list)} software")
    
    def import_groups(self):
        """Import threat actors/groups (intrusion-set)"""
        print("Importing threat actors...")
        groups = self.get_objects_by_type('intrusion-set')
        
        with self.app.app_context():
            for group_data in groups:
                external_refs = group_data.get('external_references', [])
                actor_id = None
                for ref in external_refs:
                    if ref.get('source_name') == 'mitre-attack':
                        actor_id = ref.get('external_id')
                        break
                
                if not actor_id:
                    continue
                
                # Check if actor already exists
                existing = ThreatActor.query.filter_by(actor_id=actor_id).first()
                if existing:
                    print(f"  Actor {actor_id} already exists, updating...")
                    existing.name = group_data.get('name', '')
                    existing.description = group_data.get('description', '')
                    existing.url = group_data.get('external_references', [{}])[0].get('url', '')
                else:
                    print(f"  Creating actor {actor_id}...")
                    actor = ThreatActor(
                        actor_id=actor_id,
                        name=group_data.get('name', ''),
                        description=group_data.get('description', ''),
                        url=group_data.get('external_references', [{}])[0].get('url', ''),
                        created_at=datetime.now(),
                        updated_at=datetime.now()
                    )
                    db.session.add(actor)
            
            db.session.commit()
            print(f"Imported {len(groups)} threat actors")
    
    def import_all(self, domain='enterprise'):
        """Import all ATT&CK data"""
        try:
            self.fetch_data(domain)
            self.import_tactics()
            self.import_techniques()
            self.import_mitigations()
            self.import_software()
            self.import_groups()
            print(f"\n✅ Successfully imported all {domain} ATT&CK data!")
        except Exception as e:
            print(f"\n❌ Error importing data: {e}")
            import traceback
            traceback.print_exc()

def main():
    app = create_app('development')
    
    print("=" * 60)
    print("MITRE ATT&CK Data Importer")
    print("=" * 60)
    
    importer = AttackDataImporter(app)
    
    # Import enterprise data by default
    importer.import_all('enterprise')
    
    print("\nImport completed!")

if __name__ == '__main__':
    main()
