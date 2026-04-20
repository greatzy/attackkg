from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import or_
from app import db
from app.models.rule import DetectionRule
from app.utils.decorators import admin_required, permission_required
from app.utils.helpers import paginate_response

rules_bp = Blueprint('rules', __name__)

@rules_bp.route('/rules', methods=['GET'])
@jwt_required()
def get_rules():
    """
    Get all detection rules
    ---
    tags:
      - Detection Rules
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
        description: List of detection rules
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '')
    
    query = DetectionRule.query
    
    if search:
        query = query.filter(
            or_(
                DetectionRule.name.ilike(f'%{search}%'),
                DetectionRule.description.ilike(f'%{search}%'),
                DetectionRule.rule_id.ilike(f'%{search}%')
            )
        )
    
    pagination = query.order_by(DetectionRule.name).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return paginate_response(pagination)

@rules_bp.route('/rules/<string:rule_id>', methods=['GET'])
@jwt_required()
def get_rule(rule_id):
    """
    Get a specific detection rule
    ---
    tags:
      - Detection Rules
    parameters:
      - name: rule_id
        in: path
        required: true
        type: string
    responses:
      200:
        description: Detection rule details
      404:
        description: Detection rule not found
    """
    rule = DetectionRule.query.filter_by(rule_id=rule_id).first_or_404()
    return jsonify(rule.to_dict())

@rules_bp.route('/rules', methods=['POST'])
@admin_required
def create_rule():
    """
    Create a new detection rule
    ---
    tags:
      - Detection Rules
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - rule_id
            - name
            - content
          properties:
            rule_id:
              type: string
            name:
              type: string
            description:
              type: string
            content:
              type: string
            type:
              type: string
            severity:
              type: string
            platforms:
              type: array
              items:
                type: string
            techniques:
              type: array
              items:
                type: string
    responses:
      201:
        description: Detection rule created successfully
      400:
        description: Invalid data
      409:
        description: Detection rule already exists
    """
    data = request.get_json()
    rule_id = data.get('rule_id')
    name = data.get('name')
    content = data.get('content')
    
    if not rule_id or not name or not content:
        return jsonify({'error': 'Missing required fields'}), 400
    
    if DetectionRule.query.filter_by(rule_id=rule_id).first():
        return jsonify({'error': 'Detection rule already exists'}), 409
    
    rule = DetectionRule(**data)
    db.session.add(rule)
    db.session.commit()
    
    return jsonify({
        'message': 'Detection rule created successfully',
        'rule': rule.to_dict()
    }), 201

@rules_bp.route('/rules/<string:rule_id>', methods=['PUT'])
@admin_required
def update_rule(rule_id):
    """
    Update a detection rule
    ---
    tags:
      - Detection Rules
    parameters:
      - name: rule_id
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
            description:
              type: string
            content:
              type: string
            type:
              type: string
            severity:
              type: string
            platforms:
              type: array
              items:
                type: string
            techniques:
              type: array
              items:
                type: string
    responses:
      200:
        description: Detection rule updated successfully
      404:
        description: Detection rule not found
    """
    rule = DetectionRule.query.filter_by(rule_id=rule_id).first_or_404()
    data = request.get_json()
    
    for key, value in data.items():
        if hasattr(rule, key):
            setattr(rule, key, value)
    
    db.session.commit()
    return jsonify({
        'message': 'Detection rule updated successfully',
        'rule': rule.to_dict()
    }), 200

@rules_bp.route('/rules/<string:rule_id>', methods=['DELETE'])
@admin_required
def delete_rule(rule_id):
    """
    Delete a detection rule
    ---
    tags:
      - Detection Rules
    parameters:
      - name: rule_id
        in: path
        required: true
        type: string
    responses:
      200:
        description: Detection rule deleted successfully
      404:
        description: Detection rule not found
    """
    rule = DetectionRule.query.filter_by(rule_id=rule_id).first_or_404()
    db.session.delete(rule)
    db.session.commit()
    return jsonify({'message': 'Detection rule deleted successfully'}), 200

@rules_bp.route('/rules/<string:rule_id>/test', methods=['POST'])
@jwt_required()
def test_rule(rule_id):
    """
    Test a detection rule
    ---
    tags:
      - Detection Rules
    parameters:
      - name: rule_id
        in: path
        required: true
        type: string
      - in: body
        name: body
        schema:
          type: object
          required:
            - test_data
          properties:
            test_data:
              type: string
    responses:
      200:
        description: Test results
      404:
        description: Detection rule not found
    """
    rule = DetectionRule.query.filter_by(rule_id=rule_id).first_or_404()
    data = request.get_json()
    test_data = data.get('test_data')
    
    if not test_data:
        return jsonify({'error': 'Missing test data'}), 400
    
    # 模拟规则测试
    return jsonify({
        'rule_id': rule_id,
        'name': rule.name,
        'test_result': 'passed',
        'matches': 2,
        'execution_time': 0.123
    })
