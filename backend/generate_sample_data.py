#!/usr/bin/env python
"""
Generate sample ATT&CK data for development and testing
"""

import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.attack import Tactic, Technique, Mitigation, Software
from app.models.actor import ThreatActor

def generate_tactics():
    """Generate sample tactics"""
    tactics_data = [
        {'tactic_id': 'TA0043', 'name': 'Reconnaissance', 'description': 'The adversary is trying to gather information they can use to plan future operations.'},
        {'tactic_id': 'TA0042', 'name': 'Resource Development', 'description': 'The adversary is trying to establish resources they can use to support operations.'},
        {'tactic_id': 'TA0001', 'name': 'Initial Access', 'description': 'The adversary is trying to get into your network.'},
        {'tactic_id': 'TA0002', 'name': 'Execution', 'description': 'The adversary is trying to run malicious code.'},
        {'tactic_id': 'TA0003', 'name': 'Persistence', 'description': 'The adversary is trying to maintain their foothold.'},
        {'tactic_id': 'TA0004', 'name': 'Privilege Escalation', 'description': 'The adversary is trying to gain higher-level permissions.'},
        {'tactic_id': 'TA0005', 'name': 'Defense Evasion', 'description': 'The adversary is trying to avoid being detected.'},
        {'tactic_id': 'TA0006', 'name': 'Credential Access', 'description': 'The adversary is trying to steal account names and passwords.'},
        {'tactic_id': 'TA0007', 'name': 'Discovery', 'description': 'The adversary is trying to figure out your environment.'},
        {'tactic_id': 'TA0008', 'name': 'Lateral Movement', 'description': 'The adversary is trying to move through your environment.'},
        {'tactic_id': 'TA0009', 'name': 'Collection', 'description': 'The adversary is trying to gather data of interest to their goal.'},
        {'tactic_id': 'TA0011', 'name': 'Command and Control', 'description': 'The adversary is trying to communicate with compromised systems to control them.'},
        {'tactic_id': 'TA0010', 'name': 'Exfiltration', 'description': 'The adversary is trying to steal data.'},
        {'tactic_id': 'TA0040', 'name': 'Impact', 'description': 'The adversary is trying to manipulate, interrupt, or destroy your systems and data.'},
    ]
    
    with create_app('development').app_context():
        for tactic_data in tactics_data:
            existing = Tactic.query.filter_by(tactic_id=tactic_data['tactic_id']).first()
            if not existing:
                tactic = Tactic(
                    tactic_id=tactic_data['tactic_id'],
                    name=tactic_data['name'],
                    description=tactic_data['description'],
                    url=f"https://attack.mitre.org/tactics/{tactic_data['tactic_id']}",
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                db.session.add(tactic)
                print(f"Created tactic: {tactic_data['name']}")
        
        db.session.commit()
        print(f"Generated {len(tactics_data)} tactics")

def generate_techniques():
    """Generate sample techniques"""
    techniques_data = [
        # Initial Access
        {'technique_id': 'T1566', 'name': 'Phishing', 'description': 'Adversaries may send phishing messages to gain access to victim systems.', 'tactic_id': 'TA0001', 'platforms': ['Windows', 'Linux', 'macOS']},
        {'technique_id': 'T1190', 'name': 'Exploit Public-Facing Application', 'description': 'Adversaries may attempt to take advantage of a weakness in an Internet-facing computer or program.', 'tactic_id': 'TA0001', 'platforms': ['Windows', 'Linux']},
        {'technique_id': 'T1133', 'name': 'External Remote Services', 'description': 'Adversaries may leverage external-facing remote services to initially access and/or persist within a network.', 'tactic_id': 'TA0001', 'platforms': ['Windows', 'Linux']},
        
        # Execution
        {'technique_id': 'T1059', 'name': 'Command and Scripting Interpreter', 'description': 'Adversaries may abuse command and script interpreters to execute commands, scripts, or binaries.', 'tactic_id': 'TA0002', 'platforms': ['Windows', 'Linux', 'macOS']},
        {'technique_id': 'T1053', 'name': 'Scheduled Task/Job', 'description': 'Adversaries may abuse task scheduling functionality to facilitate initial or recurring execution of malicious code.', 'tactic_id': 'TA0002', 'platforms': ['Windows', 'Linux']},
        {'technique_id': 'T1047', 'name': 'Windows Management Instrumentation', 'description': 'Adversaries may abuse Windows Management Instrumentation (WMI) to execute malicious commands and payloads.', 'tactic_id': 'TA0002', 'platforms': ['Windows']},
        
        # Persistence
        {'technique_id': 'T1547', 'name': 'Boot or Logon Autostart Execution', 'description': 'Adversaries may configure system settings to automatically execute a program during system boot or logon.', 'tactic_id': 'TA0003', 'platforms': ['Windows', 'Linux', 'macOS']},
        {'technique_id': 'T1053', 'name': 'Scheduled Task/Job', 'description': 'Adversaries may abuse task scheduling functionality to facilitate initial or recurring execution of malicious code.', 'tactic_id': 'TA0003', 'platforms': ['Windows', 'Linux']},
        {'technique_id': 'T1543', 'name': 'Create or Modify System Process', 'description': 'Adversaries may create or modify system processes to repeatedly execute malicious payloads as part of persistence.', 'tactic_id': 'TA0003', 'platforms': ['Windows', 'Linux']},
        
        # Privilege Escalation
        {'technique_id': 'T1068', 'name': 'Exploitation for Privilege Escalation', 'description': 'Adversaries may exploit software vulnerabilities in an attempt to elevate privileges.', 'tactic_id': 'TA0004', 'platforms': ['Windows', 'Linux', 'macOS']},
        {'technique_id': 'T1574', 'name': 'Hijack Execution Flow', 'description': 'Adversaries may execute their own malicious payloads by hijacking the way operating systems run programs.', 'tactic_id': 'TA0004', 'platforms': ['Windows', 'Linux']},
        
        # Defense Evasion
        {'technique_id': 'T1070', 'name': 'Indicator Removal on Host', 'description': 'Adversaries may delete or modify artifacts generated on a host system to remove evidence of their presence.', 'tactic_id': 'TA0005', 'platforms': ['Windows', 'Linux', 'macOS']},
        {'technique_id': 'T1027', 'name': 'Obfuscated Files or Information', 'description': 'Adversaries may attempt to make an executable or file difficult to discover or analyze by encrypting, encoding, or otherwise obfuscating its contents.', 'tactic_id': 'TA0005', 'platforms': ['Windows', 'Linux', 'macOS']},
        {'technique_id': 'T1055', 'name': 'Process Injection', 'description': 'Adversaries may inject code into processes in order to evade process-based defenses as well as possibly elevate privileges.', 'tactic_id': 'TA0005', 'platforms': ['Windows', 'Linux']},
        
        # Credential Access
        {'technique_id': 'T1003', 'name': 'OS Credential Dumping', 'description': 'Adversaries may attempt to dump credentials to obtain account login and credential material.', 'tactic_id': 'TA0006', 'platforms': ['Windows', 'Linux']},
        {'technique_id': 'T1110', 'name': 'Brute Force', 'description': 'Adversaries may use brute force techniques to gain access to accounts when passwords are unknown or when password hashes are obtained.', 'tactic_id': 'TA0006', 'platforms': ['Windows', 'Linux', 'macOS']},
        
        # Discovery
        {'technique_id': 'T1083', 'name': 'File and Directory Discovery', 'description': 'Adversaries may enumerate files and directories or may search in specific locations of a host or network share for certain information.', 'tactic_id': 'TA0007', 'platforms': ['Windows', 'Linux', 'macOS']},
        {'technique_id': 'T1057', 'name': 'Process Discovery', 'description': 'Adversaries may attempt to get information about running processes on a system.', 'tactic_id': 'TA0007', 'platforms': ['Windows', 'Linux', 'macOS']},
        
        # Lateral Movement
        {'technique_id': 'T1021', 'name': 'Remote Services', 'description': 'Adversaries may use Valid Accounts to log into a service specifically designed to accept remote connections.', 'tactic_id': 'TA0008', 'platforms': ['Windows', 'Linux']},
        {'technique_id': 'T1210', 'name': 'Exploitation of Remote Services', 'description': 'Adversaries may exploit remote services to gain unauthorized access to internal systems.', 'tactic_id': 'TA0008', 'platforms': ['Windows', 'Linux']},
        
        # Collection
        {'technique_id': 'T1005', 'name': 'Data from Local System', 'description': 'Adversaries may search local system sources, such as file systems or local databases, to find files of interest and sensitive data.', 'tactic_id': 'TA0009', 'platforms': ['Windows', 'Linux', 'macOS']},
        {'technique_id': 'T1114', 'name': 'Email Collection', 'description': 'Adversaries may target user email to collect sensitive information.', 'tactic_id': 'TA0009', 'platforms': ['Windows', 'Linux']},
        
        # Command and Control
        {'technique_id': 'T1071', 'name': 'Application Layer Protocol', 'description': 'Adversaries may communicate using OSI application layer protocols to avoid detection/network filtering.', 'tactic_id': 'TA0011', 'platforms': ['Windows', 'Linux', 'macOS']},
        {'technique_id': 'T1572', 'name': 'Protocol Tunneling', 'description': 'Adversaries may tunnel network communications to and from a victim system within a separate protocol.', 'tactic_id': 'TA0011', 'platforms': ['Windows', 'Linux']},
        
        # Exfiltration
        {'technique_id': 'T1041', 'name': 'Exfiltration Over C2 Channel', 'description': 'Adversaries may steal data by exfiltrating it over an existing command and control channel.', 'tactic_id': 'TA0010', 'platforms': ['Windows', 'Linux', 'macOS']},
        {'technique_id': 'T1048', 'name': 'Exfiltration Over Alternative Protocol', 'description': 'Adversaries may steal data by exfiltrating it over a different protocol than that of the existing command and control channel.', 'tactic_id': 'TA0010', 'platforms': ['Windows', 'Linux']},
        
        # Impact
        {'technique_id': 'T1496', 'name': 'Resource Hijacking', 'description': 'Adversaries may leverage the resources of co-opted systems in order to solve resource intensive problems.', 'tactic_id': 'TA0040', 'platforms': ['Windows', 'Linux']},
        {'technique_id': 'T1486', 'name': 'Data Encrypted for Impact', 'description': 'Adversaries may encrypt data on target systems or on large numbers of systems in a network to interrupt availability to system and network resources.', 'tactic_id': 'TA0040', 'platforms': ['Windows', 'Linux']},
    ]
    
    with create_app('development').app_context():
        for tech_data in techniques_data:
            existing = Technique.query.filter_by(technique_id=tech_data['technique_id']).first()
            if not existing:
                technique = Technique(
                    technique_id=tech_data['technique_id'],
                    name=tech_data['name'],
                    description=tech_data['description'],
                    url=f"https://attack.mitre.org/techniques/{tech_data['technique_id']}",
                    platforms=tech_data['platforms'],
                    is_subtechnique=False,
                    tactic_id=tech_data['tactic_id'],
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                db.session.add(technique)
                print(f"Created technique: {tech_data['name']}")
        
        db.session.commit()
        print(f"Generated {len(techniques_data)} techniques")

def generate_subtechniques():
    """Generate sample sub-techniques"""
    subtechniques_data = [
        {'technique_id': 'T1566.001', 'name': 'Spearphishing Attachment', 'description': 'Adversaries may send spearphishing emails with malicious attachments.', 'tactic_id': 'TA0001', 'platforms': ['Windows', 'Linux', 'macOS']},
        {'technique_id': 'T1566.002', 'name': 'Spearphishing Link', 'description': 'Adversaries may send spearphishing emails with malicious links.', 'tactic_id': 'TA0001', 'platforms': ['Windows', 'Linux', 'macOS']},
        {'technique_id': 'T1059.001', 'name': 'PowerShell', 'description': 'Adversaries may abuse PowerShell commands and scripts for execution.', 'tactic_id': 'TA0002', 'platforms': ['Windows']},
        {'technique_id': 'T1059.003', 'name': 'Windows Command Shell', 'description': 'Adversaries may abuse cmd.exe to execute commands.', 'tactic_id': 'TA0002', 'platforms': ['Windows']},
        {'technique_id': 'T1059.006', 'name': 'Python', 'description': 'Adversaries may abuse Python commands and scripts for execution.', 'tactic_id': 'TA0002', 'platforms': ['Windows', 'Linux', 'macOS']},
        {'technique_id': 'T1547.001', 'name': 'Registry Run Keys', 'description': 'Adversaries may achieve persistence by adding a program to a startup folder or referencing it with a Registry run key.', 'tactic_id': 'TA0003', 'platforms': ['Windows']},
        {'technique_id': 'T1003.001', 'name': 'LSASS Memory', 'description': 'Adversaries may attempt to access credential material stored in the process memory of the Local Security Authority Subsystem Service (LSASS).', 'tactic_id': 'TA0006', 'platforms': ['Windows']},
        {'technique_id': 'T1021.001', 'name': 'Remote Desktop Protocol', 'description': 'Adversaries may use Valid Accounts to log into a computer using Remote Desktop Protocol (RDP).', 'tactic_id': 'TA0008', 'platforms': ['Windows']},
        {'technique_id': 'T1021.002', 'name': 'SMB/Windows Admin Shares', 'description': 'Adversaries may use Valid Accounts to interact with a remote network share using Server Message Block (SMB).', 'tactic_id': 'TA0008', 'platforms': ['Windows']},
        {'technique_id': 'T1071.001', 'name': 'Web Protocols', 'description': 'Adversaries may communicate using application layer protocols associated with web traffic to avoid detection.', 'tactic_id': 'TA0011', 'platforms': ['Windows', 'Linux', 'macOS']},
    ]
    
    with create_app('development').app_context():
        for tech_data in subtechniques_data:
            existing = Technique.query.filter_by(technique_id=tech_data['technique_id']).first()
            if not existing:
                technique = Technique(
                    technique_id=tech_data['technique_id'],
                    name=tech_data['name'],
                    description=tech_data['description'],
                    url=f"https://attack.mitre.org/techniques/{tech_data['technique_id']}",
                    platforms=tech_data['platforms'],
                    is_subtechnique=True,
                    tactic_id=tech_data['tactic_id'],
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                db.session.add(technique)
                print(f"Created sub-technique: {tech_data['name']}")
        
        db.session.commit()
        print(f"Generated {len(subtechniques_data)} sub-techniques")

def generate_mitigations():
    """Generate sample mitigations"""
    mitigations_data = [
        {'mitigation_id': 'M1047', 'name': 'Audit', 'description': 'Perform audits or scans of systems, permissions, insecure software, insecure configurations, etc. to identify potential weaknesses.'},
        {'mitigation_id': 'M1048', 'name': 'Application Isolation and Sandboxing', 'description': 'Restrict execution of code to a virtual environment on or in transit to an endpoint system.'},
        {'mitigation_id': 'M1038', 'name': 'Execution Prevention', 'description': 'Block execution of code on a system through application control, antivirus/antimalware software, or application whitelisting.'},
        {'mitigation_id': 'M1026', 'name': 'Privileged Account Management', 'description': 'Manage the creation, modification, use, and permissions associated with privileged accounts, including SYSTEM and root.'},
        {'mitigation_id': 'M1017', 'name': 'User Training', 'description': 'Train users to be aware of access or manipulation attempts by an adversary to reduce the risk of successful spearphishing, social engineering, and other techniques.'},
    ]
    
    with create_app('development').app_context():
        for mit_data in mitigations_data:
            existing = Mitigation.query.filter_by(mitigation_id=mit_data['mitigation_id']).first()
            if not existing:
                mitigation = Mitigation(
                    mitigation_id=mit_data['mitigation_id'],
                    name=mit_data['name'],
                    description=mit_data['description'],
                    url=f"https://attack.mitre.org/mitigations/{mit_data['mitigation_id']}",
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                db.session.add(mitigation)
                print(f"Created mitigation: {mit_data['name']}")
        
        db.session.commit()
        print(f"Generated {len(mitigations_data)} mitigations")

def generate_software():
    """Generate sample software"""
    software_data = [
        {'software_id': 'S0002', 'name': 'Mimikatz', 'description': 'Mimikatz is a credential dumper capable of obtaining plaintext Windows account logins and passwords.', 'type': 'tool'},
        {'software_id': 'S0001', 'name': 'Metasploit', 'description': 'Metasploit is a computer security project that provides information about security vulnerabilities and aids in penetration testing.', 'type': 'tool'},
        {'software_id': 'S0266', 'name': 'TrickBot', 'description': 'TrickBot is a Trojan spyware program that has mainly been used for targeting banking sites.', 'type': 'malware'},
        {'software_id': 'S0366', 'name': 'WannaCry', 'description': 'WannaCry is ransomware that was first seen in a global attack during May 2017.', 'type': 'malware'},
        {'software_id': 'S0154', 'name': 'Cobalt Strike', 'description': 'Cobalt Strike is a commercial, full-featured, remote access tool that bills itself as "adversary simulation software".', 'type': 'tool'},
    ]
    
    with create_app('development').app_context():
        for sw_data in software_data:
            existing = Software.query.filter_by(software_id=sw_data['software_id']).first()
            if not existing:
                software = Software(
                    software_id=sw_data['software_id'],
                    name=sw_data['name'],
                    description=sw_data['description'],
                    type=sw_data['type'],
                    url=f"https://attack.mitre.org/software/{sw_data['software_id']}",
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                db.session.add(software)
                print(f"Created software: {sw_data['name']}")
        
        db.session.commit()
        print(f"Generated {len(software_data)} software")

def generate_actors():
    """Generate sample threat actors"""
    actors_data = [
        {'actor_id': 'G0001', 'name': 'APT28', 'description': 'APT28 is a threat group that has been attributed to Russia\'s General Staff Main Intelligence Directorate (GRU).'},
        {'actor_id': 'G0007', 'name': 'APT28', 'description': 'APT29 is a threat group that has been attributed to Russia\'s Foreign Intelligence Service (SVR).'},
        {'actor_id': 'G0032', 'name': 'Lazarus Group', 'description': 'Lazarus Group is a North Korean state-sponsored cyber threat group.'},
        {'actor_id': 'G0089', 'name': 'Kimsuky', 'description': 'Kimsuky is a North Korean state-sponsored cyber threat group.'},
        {'actor_id': 'G0050', 'name': 'APT32', 'description': 'APT32 is a threat group that has been active since at least 2012.'},
    ]
    
    with create_app('development').app_context():
        for actor_data in actors_data:
            existing = ThreatActor.query.filter_by(actor_id=actor_data['actor_id']).first()
            if not existing:
                actor = ThreatActor(
                    actor_id=actor_data['actor_id'],
                    name=actor_data['name'],
                    description=actor_data['description'],
                    url=f"https://attack.mitre.org/groups/{actor_data['actor_id']}",
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                db.session.add(actor)
                print(f"Created actor: {actor_data['name']}")
        
        db.session.commit()
        print(f"Generated {len(actors_data)} actors")

def main():
    print("=" * 60)
    print("Generating Sample ATT&CK Data")
    print("=" * 60)
    
    generate_tactics()
    generate_techniques()
    generate_subtechniques()
    generate_mitigations()
    generate_software()
    generate_actors()
    
    print("\n✅ Sample data generation completed!")

if __name__ == '__main__':
    main()
