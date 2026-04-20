from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import or_
from app import db
from app.models.report import Report
from app.utils.decorators import admin_required, permission_required
from app.utils.helpers import paginate_response

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/reports', methods=['GET'])
@jwt_required()
def get_reports():
    """
    Get all reports
    ---
    tags:
      - Reports
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
        description: List of reports
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '')
    
    query = Report.query
    
    if search:
        query = query.filter(
            or_(
                Report.title.ilike(f'%{search}%'),
                Report.description.ilike(f'%{search}%')
            )
        )
    
    pagination = query.order_by(Report.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return paginate_response(pagination)

@reports_bp.route('/reports/<int:report_id>', methods=['GET'])
@jwt_required()
def get_report(report_id):
    """
    Get a specific report
    ---
    tags:
      - Reports
    parameters:
      - name: report_id
        in: path
        required: true
        type: integer
    responses:
      200:
        description: Report details
      404:
        description: Report not found
    """
    report = Report.query.get_or_404(report_id)
    return jsonify(report.to_dict())

@reports_bp.route('/reports', methods=['POST'])
@admin_required
def create_report():
    """
    Create a new report
    ---
    tags:
      - Reports
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - title
          properties:
            title:
              type: string
            description:
              type: string
            content:
              type: string
            template:
              type: string
            parameters:
              type: object
            status:
              type: string
    responses:
      201:
        description: Report created successfully
      400:
        description: Invalid data
    """
    data = request.get_json()
    title = data.get('title')
    
    if not title:
        return jsonify({'error': 'Missing required fields'}), 400
    
    report = Report(**data)
    db.session.add(report)
    db.session.commit()
    
    return jsonify({
        'message': 'Report created successfully',
        'report': report.to_dict()
    }), 201

@reports_bp.route('/reports/<int:report_id>', methods=['PUT'])
@admin_required
def update_report(report_id):
    """
    Update a report
    ---
    tags:
      - Reports
    parameters:
      - name: report_id
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
            template:
              type: string
            parameters:
              type: object
            status:
              type: string
    responses:
      200:
        description: Report updated successfully
      404:
        description: Report not found
    """
    report = Report.query.get_or_404(report_id)
    data = request.get_json()
    
    for key, value in data.items():
        if hasattr(report, key):
            setattr(report, key, value)
    
    db.session.commit()
    return jsonify({
        'message': 'Report updated successfully',
        'report': report.to_dict()
    }), 200

@reports_bp.route('/reports/<int:report_id>', methods=['DELETE'])
@admin_required
def delete_report(report_id):
    """
    Delete a report
    ---
    tags:
      - Reports
    parameters:
      - name: report_id
        in: path
        required: true
        type: integer
    responses:
      200:
        description: Report deleted successfully
      404:
        description: Report not found
    """
    report = Report.query.get_or_404(report_id)
    db.session.delete(report)
    db.session.commit()
    return jsonify({'message': 'Report deleted successfully'}), 200

@reports_bp.route('/reports/<int:report_id>/generate', methods=['POST'])
@jwt_required()
def generate_report(report_id):
    """
    Generate a report
    ---
    tags:
      - Reports
    parameters:
      - name: report_id
        in: path
        required: true
        type: integer
    responses:
      200:
        description: Report generated successfully
      404:
        description: Report not found
    """
    report = Report.query.get_or_404(report_id)
    # 模拟报告生成
    return jsonify({
        'report_id': report_id,
        'name': report.title,
        'status': 'generated',
        'download_url': f'/api/reports/{report_id}/download'
    })

@reports_bp.route('/reports/<int:report_id>/download', methods=['GET'])
@jwt_required()
def download_report(report_id):
    """
    Download a report
    ---
    tags:
      - Reports
    parameters:
      - name: report_id
        in: path
        required: true
        type: integer
    responses:
      200:
        description: Report file
      404:
        description: Report not found
    """
    report = Report.query.get_or_404(report_id)
    # 模拟文件下载
    return jsonify({'message': 'Report download not implemented yet'}), 501
