from flask import Blueprint, request, jsonify
from sqlalchemy import or_
from app import db
from app.models.attack import Tactic, Technique
from app.utils.helpers import paginate_response

visualization_bp = Blueprint('visualization', __name__)

@visualization_bp.route('/visualization/attack_matrix', methods=['GET'])
def get_attack_matrix():
    """
    Get ATT&CK matrix data
    ---
    tags:
      - Visualization
    parameters:
      - name: platform
        in: query
        type: string
    responses:
      200:
        description: Attack matrix data
    """
    platform = request.args.get('platform')
    
    # 获取所有战术和技术
    tactics = Tactic.query.all()
    matrix_data = []
    
    for tactic in tactics:
        tactic_data = tactic.to_dict()
        if platform:
            tactic_data['techniques'] = Technique.query.filter(
                Technique.tactic_id == tactic.tactic_id,
                Technique.platforms.contains([platform])
            ).all()
        else:
            tactic_data['techniques'] = tactic.techniques.all()
            
        tactic_data['techniques'] = [t.to_dict() for t in tactic_data['techniques']]
        matrix_data.append(tactic_data)
    
    return jsonify({
        'matrix': matrix_data,
        'total_tactics': len(tactics),
        'total_techniques': Technique.query.count()
    })

@visualization_bp.route('/visualization/techniques_by_tactic', methods=['GET'])
def get_techniques_by_tactic():
    """
    Get techniques by tactic
    ---
    tags:
      - Visualization
    responses:
      200:
        description: Techniques by tactic
    """
    # 模拟数据
    tactics = Tactic.query.all()
    data = []
    
    for tactic in tactics:
        data.append({
            'name': tactic.name,
            'id': tactic.tactic_id,
            'techniques': tactic.techniques.count()
        })
    
    return jsonify(data)

@visualization_bp.route('/visualization/techniques_by_platform', methods=['GET'])
def get_techniques_by_platform():
    """
    Get techniques by platform
    ---
    tags:
      - Visualization
    responses:
      200:
        description: Techniques by platform
    """
    # 模拟数据
    platforms = ['Windows', 'Linux', 'MacOS', 'Network', 'Azure AD']
    data = []
    
    for platform in platforms:
        count = Technique.query.filter(Technique.platforms.contains([platform])).count()
        data.append({
            'name': platform,
            'count': count
        })
    
    return jsonify(data)

@visualization_bp.route('/visualization/mitigations_statistics', methods=['GET'])
def get_mitigations_statistics():
    """
    Get mitigations statistics
    ---
    tags:
      - Visualization
    responses:
      200:
        description: Mitigations statistics
    """
    # 模拟数据
    return jsonify({
        'total_mitigations': 40,
        'most_used_techniques': [
            { 'name': 'MITRE-AT-001', 'count': 25 },
            { 'name': 'MITRE-AT-002', 'count': 18 },
            { 'name': 'MITRE-AT-003', 'count': 15 }
        ],
        'mitigations_by_category': {
            'Network': 15,
            'Endpoint': 12,
            'Application': 8,
            'Data': 5
        }
    })

@visualization_bp.route('/visualization/attack_paths', methods=['GET'])
def get_attack_paths():
    """
    Get attack paths graph data
    ---
    tags:
      - Visualization
    parameters:
      - name: actor_id
        in: query
        type: string
        description: Filter by threat actor
      - name: tactic_id
        in: query
        type: string
        description: Filter by tactic
    responses:
      200:
        description: Attack paths graph data with nodes and edges
    """
    from app.models.actor import ThreatActor
    
    actor_id = request.args.get('actor_id')
    tactic_id = request.args.get('tactic_id')
    
    # Build query for techniques
    query = Technique.query
    if tactic_id:
        query = query.filter_by(tactic_id=tactic_id)
    
    techniques = query.all()
    
    # Get tactics for nodes
    tactics = Tactic.query.all()
    
    # Build nodes (tactics and techniques)
    nodes = []
    
    # Add tactic nodes
    for tactic in tactics:
        if not tactic_id or tactic.tactic_id == tactic_id:
            nodes.append({
                'id': tactic.tactic_id,
                'name': tactic.name,
                'type': 'tactic',
                'category': tactic.tactic_id,
                'value': tactic.techniques.count()
            })
    
    # Add technique nodes
    for technique in techniques:
        nodes.append({
            'id': technique.technique_id,
            'name': technique.name,
            'type': 'technique',
            'category': technique.tactic_id or 'unknown',
            'value': 1,
            'is_subtechnique': technique.is_subtechnique
        })
    
    # Build edges (relationships)
    edges = []
    
    # Connect techniques to their tactics
    for technique in techniques:
        if technique.tactic_id:
            edges.append({
                'source': technique.tactic_id,
                'target': technique.technique_id,
                'type': 'belongs_to'
            })
    
    # Add some common attack path patterns
    # These are example patterns based on common attack chains
    attack_patterns = [
        # Initial Access -> Execution
        ('T1566', 'T1059'),  # Phishing -> Command and Scripting Interpreter
        ('T1190', 'T1059'),  # Exploit Public-Facing Application -> Command and Scripting Interpreter
        # Execution -> Persistence
        ('T1059', 'T1547'),  # Command and Scripting Interpreter -> Boot or Logon Autostart Execution
        ('T1059', 'T1053'),  # Command and Scripting Interpreter -> Scheduled Task/Job
        # Persistence -> Privilege Escalation
        ('T1547', 'T1068'),  # Boot or Logon Autostart Execution -> Exploitation for Privilege Escalation
        # Privilege Escalation -> Defense Evasion
        ('T1068', 'T1070'),  # Exploitation for Privilege Escalation -> Indicator Removal on Host
        ('T1068', 'T1027'),  # Exploitation for Privilege Escalation -> Obfuscated Files or Information
        # Defense Evasion -> Credential Access
        ('T1070', 'T1003'),  # Indicator Removal on Host -> OS Credential Dumping
        ('T1027', 'T1003'),  # Obfuscated Files or Information -> OS Credential Dumping
        # Credential Access -> Lateral Movement
        ('T1003', 'T1021'),  # OS Credential Dumping -> Remote Services
        # Lateral Movement -> Collection
        ('T1021', 'T1005'),  # Remote Services -> Data from Local System
        # Collection -> Exfiltration
        ('T1005', 'T1041'),  # Data from Local System -> Exfiltration Over C2 Channel
        # Exfiltration -> Impact
        ('T1041', 'T1496'),  # Exfiltration Over C2 Channel -> Resource Hijacking
    ]
    
    for source_id, target_id in attack_patterns:
        # Check if both techniques exist in our dataset
        source_exists = any(n['id'] == source_id for n in nodes)
        target_exists = any(n['id'] == target_id for n in nodes)
        
        if source_exists and target_exists:
            edges.append({
                'source': source_id,
                'target': target_id,
                'type': 'leads_to'
            })
    
    return jsonify({
        'nodes': nodes,
        'edges': edges,
        'total_nodes': len(nodes),
        'total_edges': len(edges)
    })

@visualization_bp.route('/visualization/dashboard', methods=['GET'])
def get_dashboard_data():
    """
    Get dashboard visualization data
    ---
    tags:
      - Visualization
    responses:
      200:
        description: Dashboard data
    """
    # 模拟数据
    return jsonify({
        'stats': {
            'tactics': Tactic.query.count(),
            'techniques': Technique.query.filter_by(is_subtechnique=False).count(),
            'subtechniques': Technique.query.filter_by(is_subtechnique=True).count(),
            'mitigations': Technique.query.filter(Technique.mitigations.any()).count(),
            'rules': 0,
            'actors': 0
        },
        'recent_activity': [
            {
                'type': 'technique',
                'id': 'MITRE-AT-001',
                'name': 'Phishing',
                'timestamp': '2024-01-19T10:30:00',
                'action': 'created'
            },
            {
                'type': 'rule',
                'id': 'rule-001',
                'name': 'Phishing Detection Rule',
                'timestamp': '2024-01-18T16:45:00',
                'action': 'updated'
            }
        ],
        'risk_scores': {
            'high': 5,
            'medium': 12,
            'low': 8
        }
    })
