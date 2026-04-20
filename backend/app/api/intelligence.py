from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import or_
from app import db
from app.models.intelligence import ThreatIntelligence
from app.utils.decorators import admin_required, permission_required
from app.utils.helpers import paginate_response

intelligence_bp = Blueprint('intelligence', __name__)

@intelligence_bp.route('/intelligence', methods=['GET'])
@jwt_required()
def get_intelligence():
    """
    Get all threat intelligence
    ---
    tags:
      - Threat Intelligence
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
        description: List of threat intelligence
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '')
    
    query = ThreatIntelligence.query
    
    if search:
        query = query.filter(
            or_(
                ThreatIntelligence.title.ilike(f'%{search}%'),
                ThreatIntelligence.description.ilike(f'%{search}%'),
                ThreatIntelligence.source.ilike(f'%{search}%')
            )
        )
    
    pagination = query.order_by(ThreatIntelligence.published_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return paginate_response(pagination)

@intelligence_bp.route('/intelligence/<int:intelligence_id>', methods=['GET'])
@jwt_required()
def get_intelligence_item(intelligence_id):
    """
    Get a specific threat intelligence item
    ---
    tags:
      - Threat Intelligence
    parameters:
      - name: intelligence_id
        in: path
        required: true
        type: integer
    responses:
      200:
        description: Threat intelligence details
      404:
        description: Threat intelligence not found
    """
    item = ThreatIntelligence.query.get_or_404(intelligence_id)
    return jsonify(item.to_dict())

@intelligence_bp.route('/intelligence', methods=['POST'])
@admin_required
def create_intelligence():
    """
    Create a new threat intelligence item
    ---
    tags:
      - Threat Intelligence
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - title
            - description
          properties:
            title:
              type: string
            description:
              type: string
            content:
              type: string
            source:
              type: string
            severity:
              type: string
            category:
              type: string
            tags:
              type: array
              items:
                type: string
            published_at:
              type: string
            references:
              type: array
              items:
                type: string
    responses:
      201:
        description: Threat intelligence created successfully
      400:
        description: Invalid data
    """
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    
    if not title or not description:
        return jsonify({'error': 'Missing required fields'}), 400
    
    item = ThreatIntelligence(**data)
    db.session.add(item)
    db.session.commit()
    
    return jsonify({
        'message': 'Threat intelligence created successfully',
        'intelligence': item.to_dict()
    }), 201

@intelligence_bp.route('/intelligence/<int:intelligence_id>', methods=['PUT'])
@admin_required
def update_intelligence(intelligence_id):
    """
    Update a threat intelligence item
    ---
    tags:
      - Threat Intelligence
    parameters:
      - name: intelligence_id
        in: path
        required: true
        type: integer
      - in: body
        name: body
        schema:
          type: object
          properties:
            title:
              type: string
            description:
              type: string
            content:
              type: string
            source:
              type: string
            severity:
              type: string
            category:
              type: string
            tags:
              type: array
              items:
                type: string
            published_at:
              type: string
            references:
              type: array
              items:
                type: string
    responses:
      200:
        description: Threat intelligence updated successfully
      404:
        description: Threat intelligence not found
    """
    item = ThreatIntelligence.query.get_or_404(intelligence_id)
    data = request.get_json()
    
    for key, value in data.items():
        if hasattr(item, key):
            setattr(item, key, value)
    
    db.session.commit()
    return jsonify({
        'message': 'Threat intelligence updated successfully',
        'intelligence': item.to_dict()
    }), 200

@intelligence_bp.route('/intelligence/<int:intelligence_id>', methods=['DELETE'])
@admin_required
def delete_intelligence(intelligence_id):
    """
    Delete a threat intelligence item
    ---
    tags:
      - Threat Intelligence
    parameters:
      - name: intelligence_id
        in: path
        required: true
        type: integer
    responses:
      200:
        description: Threat intelligence deleted successfully
      404:
        description: Threat intelligence not found
    """
    item = ThreatIntelligence.query.get_or_404(intelligence_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Threat intelligence deleted successfully'}), 200

@intelligence_bp.route('/intelligence/statistics', methods=['GET'])
@jwt_required()
def get_intelligence_statistics():
    """
    Get threat intelligence statistics
    ---
    tags:
      - Threat Intelligence
    responses:
      200:
        description: Threat intelligence statistics
    """
    # 模拟统计数据
    total = ThreatIntelligence.query.count()
    by_severity = db.session.query(
        ThreatIntelligence.severity,
        db.func.count(ThreatIntelligence.id)
    ).group_by(ThreatIntelligence.severity).all()
    
    by_threat_type = db.session.query(
        ThreatIntelligence.threat_type,
        db.func.count(ThreatIntelligence.id)
    ).group_by(ThreatIntelligence.threat_type).all()
    
    return jsonify({
        'total': total,
        'by_severity': dict(by_severity),
        'by_threat_type': dict(by_threat_type)
    })

@intelligence_bp.route('/intelligence/top_sources', methods=['GET'])
@jwt_required()
def get_top_sources():
    """
    Get top intelligence sources
    ---
    tags:
      - Threat Intelligence
    responses:
      200:
        description: Top intelligence sources
    """
    # 模拟数据
    sources = db.session.query(
        ThreatIntelligence.source,
        db.func.count(ThreatIntelligence.id)
    ).group_by(ThreatIntelligence.source).order_by(db.func.count(ThreatIntelligence.id).desc()).limit(5).all()
    
    return jsonify([{'source': s, 'count': c} for s, c in sources])
