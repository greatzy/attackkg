from flask import Blueprint, request, jsonify, current_app
from sqlalchemy import or_, func
from sqlalchemy.orm import selectinload
from app import db
from app.models.attack import Tactic, Technique, SubTechnique, Mitigation, Software
from app.utils.decorators import admin_required, permission_required
from app.utils.helpers import paginate_response
from app.utils.cache import cached

attack_bp = Blueprint('attack', __name__)

# ==================== Tactics ====================

@attack_bp.route('/tactics', methods=['GET'])
def get_tactics():
    """
    Get all tactics
    ---
    tags:
      - ATT&CK Data
    parameters:
      - name: page
        in: query
        type: integer
        default: 1
      - name: per_page
        in: query
        type: integer
        default: 20
      - name: search
        in: query
        type: string
    responses:
      200:
        description: List of tactics
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '')
    
    query = Tactic.query
    
    if search:
        search_pattern = f'%{search}%'
        query = query.filter(
            or_(
                Tactic.name.ilike(search_pattern),
                Tactic.description.ilike(search_pattern)
            )
        )
    
    pagination = query.order_by(Tactic.tactic_id).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return paginate_response(pagination, include_counts=False)

@attack_bp.route('/tactics/<string:tactic_id>', methods=['GET'])
def get_tactic(tactic_id):
    """Get tactic by ID"""
    tactic = Tactic.query.filter_by(tactic_id=tactic_id).first_or_404()
    return jsonify(tactic.to_dict())

@attack_bp.route('/tactics/<string:tactic_id>/techniques', methods=['GET'])
def get_tactic_techniques(tactic_id):
    """Get techniques for a tactic"""
    tactic = Tactic.query.filter_by(tactic_id=tactic_id).first_or_404()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    pagination = tactic.techniques.paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return paginate_response(pagination)

# ==================== Techniques ====================

@attack_bp.route('/techniques', methods=['GET'])
def get_techniques():
    """
    Get all techniques
    ---
    tags:
      - ATT&CK Data
    parameters:
      - name: page
        in: query
        type: integer
      - name: per_page
        in: query
        type: integer
      - name: search
        in: query
        type: string
      - name: tactic_id
        in: query
        type: string
      - name: platform
        in: query
        type: string
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '')
    tactic_id = request.args.get('tactic_id')
    platform = request.args.get('platform')
    
    query = Technique.query.filter_by(is_subtechnique=False)
    
    if search:
        search_pattern = f'%{search}%'
        query = query.filter(
            or_(
                Technique.name.ilike(search_pattern),
                Technique.description.ilike(search_pattern),
                Technique.technique_id.ilike(search_pattern)
            )
        )
    
    if tactic_id:
        query = query.filter_by(tactic_id=tactic_id)
    
    if platform:
        query = query.filter(Technique.platforms.contains([platform]))
    
    pagination = query.order_by(Technique.technique_id).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return paginate_response(pagination)

@attack_bp.route('/techniques/<string:technique_id>', methods=['GET'])
def get_technique(technique_id):
    """Get technique by ID"""
    technique = Technique.query.filter_by(technique_id=technique_id).first_or_404()
    data = technique.to_dict()
    
    # Include subtechniques
    data['subtechniques'] = [st.to_dict() for st in technique.subtechniques]
    
    # Include mitigations
    data['mitigations'] = [m.to_dict() for m in technique.mitigations]
    
    return jsonify(data)

@attack_bp.route('/techniques/<string:technique_id>/subtechniques', methods=['GET'])
def get_technique_subtechniques(technique_id):
    """Get subtechniques for a technique"""
    technique = Technique.query.filter_by(technique_id=technique_id).first_or_404()
    subtechniques = technique.subtechniques.all()
    return jsonify([st.to_dict() for st in subtechniques])

# ==================== SubTechniques ====================

@attack_bp.route('/subtechniques', methods=['GET'])
def get_subtechniques():
    """Get all subtechniques"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    technique_id = request.args.get('technique_id')
    
    query = SubTechnique.query
    
    if technique_id:
        query = query.filter_by(technique_id=technique_id)
    
    pagination = query.order_by(SubTechnique.subtechnique_id).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return paginate_response(pagination)

@attack_bp.route('/subtechniques/<string:subtechnique_id>', methods=['GET'])
def get_subtechnique(subtechnique_id):
    """Get subtechnique by ID"""
    subtechnique = SubTechnique.query.filter_by(subtechnique_id=subtechnique_id).first_or_404()
    return jsonify(subtechnique.to_dict())

# ==================== Mitigations ====================

@attack_bp.route('/mitigations', methods=['GET'])
def get_mitigations():
    """Get all mitigations"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '')
    
    query = Mitigation.query
    
    if search:
        query = query.filter(
            or_(
                Mitigation.name.ilike(f'%{search}%'),
                Mitigation.description.ilike(f'%{search}%')
            )
        )
    
    pagination = query.order_by(Mitigation.mitigation_id).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return paginate_response(pagination)

@attack_bp.route('/mitigations/<string:mitigation_id>', methods=['GET'])
def get_mitigation(mitigation_id):
    """Get mitigation by ID"""
    mitigation = Mitigation.query.filter_by(mitigation_id=mitigation_id).first_or_404()
    data = mitigation.to_dict()
    data['techniques'] = [t.to_dict() for t in mitigation.techniques]
    return jsonify(data)

# ==================== Software ====================

@attack_bp.route('/software', methods=['GET'])
def get_software():
    """Get all software"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '')
    software_type = request.args.get('type')
    
    query = Software.query
    
    if search:
        query = query.filter(
            or_(
                Software.name.ilike(f'%{search}%'),
                Software.description.ilike(f'%{search}%')
            )
        )
    
    if software_type:
        query = query.filter_by(type=software_type)
    
    pagination = query.order_by(Software.software_id).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return paginate_response(pagination)

@attack_bp.route('/software/<string:software_id>', methods=['GET'])
def get_software_by_id(software_id):
    """Get software by ID"""
    software = Software.query.filter_by(software_id=software_id).first_or_404()
    return jsonify(software.to_dict())

# ==================== Search ====================

@attack_bp.route('/search', methods=['GET'])
def search_attack():
    """Global search across all ATT&CK data"""
    query_str = request.args.get('q', '')
    if not query_str or len(query_str) < 2:
        return jsonify({'error': 'Search query must be at least 2 characters'}), 400
    
    search_pattern = f'%{query_str}%'
    
    # Search tactics
    tactics = Tactic.query.filter(
        or_(
            Tactic.name.ilike(search_pattern),
            Tactic.description.ilike(search_pattern)
        )
    ).limit(10).all()
    
    # Search techniques
    techniques = Technique.query.filter(
        or_(
            Technique.name.ilike(search_pattern),
            Technique.description.ilike(search_pattern),
            Technique.technique_id.ilike(search_pattern)
        )
    ).limit(10).all()
    
    # Search software
    software = Software.query.filter(
        or_(
            Software.name.ilike(search_pattern),
            Software.description.ilike(search_pattern)
        )
    ).limit(10).all()
    
    return jsonify({
        'tactics': [t.to_dict() for t in tactics],
        'techniques': [t.to_dict() for t in techniques],
        'software': [s.to_dict() for s in software],
        'total': len(tactics) + len(techniques) + len(software)
    })

# ==================== Statistics ====================

@attack_bp.route('/statistics', methods=['GET'])
@cached(timeout=600, prefix='stats')
def get_statistics():
    """Get ATT&CK statistics"""
    stats = {
        'tactics': Tactic.query.count(),
        'techniques': Technique.query.filter_by(is_subtechnique=False).count(),
        'subtechniques': SubTechnique.query.count(),
        'mitigations': Mitigation.query.count(),
        'software': {
            'total': Software.query.count(),
            'malware': Software.query.filter_by(type='malware').count(),
            'tools': Software.query.filter_by(type='tool').count()
        },
        'platforms': 0
    }
    return jsonify(stats)
