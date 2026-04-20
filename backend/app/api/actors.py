from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import or_
from app import db
from app.models.actor import ThreatActor
from app.utils.decorators import admin_required, permission_required
from app.utils.helpers import paginate_response

actors_bp = Blueprint('actors', __name__)

@actors_bp.route('/actors', methods=['GET'])
@jwt_required()
def get_actors():
    """
    Get all threat actors
    ---
    tags:
      - Threat Actors
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
        description: List of threat actors
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '')
    
    query = ThreatActor.query
    
    if search:
        query = query.filter(
            or_(
                ThreatActor.name.ilike(f'%{search}%'),
                ThreatActor.alias.ilike(f'%{search}%'),
                ThreatActor.description.ilike(f'%{search}%')
            )
        )
    
    pagination = query.order_by(ThreatActor.name).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return paginate_response(pagination)

@actors_bp.route('/actors/<string:actor_id>', methods=['GET'])
@jwt_required()
def get_actor(actor_id):
    """
    Get a specific threat actor
    ---
    tags:
      - Threat Actors
    parameters:
      - name: actor_id
        in: path
        required: true
        type: string
    responses:
      200:
        description: Threat actor details
      404:
        description: Threat actor not found
    """
    actor = ThreatActor.query.filter_by(actor_id=actor_id).first_or_404()
    return jsonify(actor.to_dict())

@actors_bp.route('/actors', methods=['POST'])
@admin_required
def create_actor():
    """
    Create a new threat actor
    ---
    tags:
      - Threat Actors
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - actor_id
            - name
          properties:
            actor_id:
              type: string
            name:
              type: string
            alias:
              type: string
            description:
              type: string
            sophistication:
              type: string
            primary_motivation:
              type: string
            secondary_motivations:
              type: array
              items:
                type: string
            targets:
              type: array
              items:
                type: string
            country:
              type: string
            techniques:
              type: array
              items:
                type: string
    responses:
      201:
        description: Threat actor created successfully
      400:
        description: Invalid data
      409:
        description: Threat actor already exists
    """
    data = request.get_json()
    actor_id = data.get('actor_id')
    name = data.get('name')
    
    if not actor_id or not name:
        return jsonify({'error': 'Missing required fields'}), 400
    
    if ThreatActor.query.filter_by(actor_id=actor_id).first():
        return jsonify({'error': 'Threat actor already exists'}), 409
    
    actor = ThreatActor(**data)
    db.session.add(actor)
    db.session.commit()
    
    return jsonify({
        'message': 'Threat actor created successfully',
        'actor': actor.to_dict()
    }), 201

@actors_bp.route('/actors/<string:actor_id>', methods=['PUT'])
@admin_required
def update_actor(actor_id):
    """
    Update a threat actor
    ---
    tags:
      - Threat Actors
    parameters:
      - name: actor_id
        in: path
        required: true
        type: string
      - in: body
        name: body
        schema:
          type: object
          properties:
            name:
              type: string
            alias:
              type: string
            description:
              type: string
            sophistication:
              type: string
            primary_motivation:
              type: string
            secondary_motivations:
              type: array
              items:
                type: string
            targets:
              type: array
              items:
                type: string
            country:
              type: string
            techniques:
              type: array
              items:
                type: string
    responses:
      200:
        description: Threat actor updated successfully
      404:
        description: Threat actor not found
    """
    actor = ThreatActor.query.filter_by(actor_id=actor_id).first_or_404()
    data = request.get_json()
    
    for key, value in data.items():
        if hasattr(actor, key):
            setattr(actor, key, value)
    
    db.session.commit()
    return jsonify({
        'message': 'Threat actor updated successfully',
        'actor': actor.to_dict()
    }), 200

@actors_bp.route('/actors/<string:actor_id>', methods=['DELETE'])
@admin_required
def delete_actor(actor_id):
    """
    Delete a threat actor
    ---
    tags:
      - Threat Actors
    parameters:
      - name: actor_id
        in: path
        required: true
        type: string
    responses:
      200:
        description: Threat actor deleted successfully
      404:
        description: Threat actor not found
    """
    actor = ThreatActor.query.filter_by(actor_id=actor_id).first_or_404()
    db.session.delete(actor)
    db.session.commit()
    return jsonify({'message': 'Threat actor deleted successfully'}), 200

@actors_bp.route('/actors/<string:actor_id>/techniques', methods=['GET'])
@jwt_required()
def get_actor_techniques(actor_id):
    """
    Get techniques associated with a threat actor
    ---
    tags:
      - Threat Actors
    parameters:
      - name: actor_id
        in: path
        required: true
        type: string
    responses:
      200:
        description: List of techniques
    """
    actor = ThreatActor.query.filter_by(actor_id=actor_id).first_or_404()
    return jsonify(actor.techniques)
