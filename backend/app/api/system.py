from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import or_
from app import db
from app.models.user import User, Role, Permission
from app.models.log import OperationLog
from app.utils.decorators import admin_required, permission_required
from app.utils.helpers import paginate_response

system_bp = Blueprint('system', __name__)

@system_bp.route('/system/users', methods=['GET'])
@admin_required
def get_users():
    """
    Get all users
    ---
    tags:
      - System
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
        description: List of users
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '')
    
    query = User.query
    
    if search:
        query = query.filter(
            or_(
                User.username.ilike(f'%{search}%'),
                User.email.ilike(f'%{search}%')
            )
        )
    
    pagination = query.order_by(User.username).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return paginate_response(pagination)

@system_bp.route('/system/users/<int:user_id>', methods=['GET'])
@admin_required
def get_user(user_id):
    """
    Get a specific user
    ---
    tags:
      - System
    parameters:
      - name: user_id
        in: path
        required: true
        type: integer
    responses:
      200:
        description: User details
      404:
        description: User not found
    """
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@system_bp.route('/system/users', methods=['POST'])
@admin_required
def create_user():
    """
    Create a new user
    ---
    tags:
      - System
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - username
            - email
            - password
          properties:
            username:
              type: string
            email:
              type: string
            password:
              type: string
            role_id:
              type: integer
    responses:
      201:
        description: User created successfully
      400:
        description: Invalid data
    """
    from werkzeug.security import generate_password_hash
    
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not username or not email or not password:
        return jsonify({'error': 'Missing required fields'}), 400
    
    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({'error': 'User already exists'}), 409
    
    user = User(
        username=username,
        email=email,
        password_hash=generate_password_hash(password),
        role_id=data.get('role_id', 2)
    )
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'message': 'User created successfully',
        'user': user.to_dict()
    }), 201

@system_bp.route('/system/users/<int:user_id>', methods=['PUT'])
@admin_required
def update_user(user_id):
    """
    Update a user
    ---
    tags:
      - System
    parameters:
      - name: user_id
        in: path
        required: true
        type: integer
      - in: body
        name: body
        schema:
          type: object
          properties:
            username:
              type: string
            email:
              type: string
            role_id:
              type: integer
            password:
              type: string
    responses:
      200:
        description: User updated successfully
      404:
        description: User not found
    """
    from werkzeug.security import generate_password_hash
    
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    if 'username' in data:
        if User.query.filter_by(username=data['username']).filter(User.id != user_id).first():
            return jsonify({'error': 'Username already exists'}), 409
        user.username = data['username']
    
    if 'email' in data:
        if User.query.filter_by(email=data['email']).filter(User.id != user_id).first():
            return jsonify({'error': 'Email already exists'}), 409
        user.email = data['email']
    
    if 'role_id' in data:
        user.role_id = data['role_id']
    
    if 'password' in data and data['password']:
        user.password_hash = generate_password_hash(data['password'])
    
    db.session.commit()
    
    return jsonify({
        'message': 'User updated successfully',
        'user': user.to_dict()
    }), 200

@system_bp.route('/system/users/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    """
    Delete a user
    ---
    tags:
      - System
    parameters:
      - name: user_id
        in: path
        required: true
        type: integer
    responses:
      200:
        description: User deleted successfully
      404:
        description: User not found
    """
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200

@system_bp.route('/system/roles', methods=['GET'])
@jwt_required()
def get_roles():
    """
    Get all roles
    ---
    tags:
      - System
    responses:
      200:
        description: List of roles
    """
    roles = Role.query.all()
    return jsonify([role.to_dict() for role in roles])

@system_bp.route('/system/roles/<int:role_id>', methods=['GET'])
@jwt_required()
def get_role(role_id):
    """
    Get a specific role
    ---
    tags:
      - System
    parameters:
      - name: role_id
        in: path
        required: true
        type: integer
    responses:
      200:
        description: Role details
      404:
        description: Role not found
    """
    role = Role.query.get_or_404(role_id)
    return jsonify(role.to_dict())

@system_bp.route('/system/roles', methods=['POST'])
@admin_required
def create_role():
    """
    Create a new role
    ---
    tags:
      - System
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - name
            - description
          properties:
            name:
              type: string
            description:
              type: string
            permissions:
              type: array
              items:
                type: integer
    responses:
      201:
        description: Role created successfully
      400:
        description: Invalid data
    """
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    
    if not name or not description:
        return jsonify({'error': 'Missing required fields'}), 400
    
    if Role.query.filter_by(name=name).first():
        return jsonify({'error': 'Role already exists'}), 409
    
    role = Role(name=name, description=description)
    db.session.add(role)
    db.session.commit()
    
    return jsonify({
        'message': 'Role created successfully',
        'role': role.to_dict()
    }), 201

@system_bp.route('/system/roles/<int:role_id>', methods=['PUT'])
@admin_required
def update_role(role_id):
    """
    Update a role
    ---
    tags:
      - System
    parameters:
      - name: role_id
        in: path
        required: true
        type: integer
      - in: body
        name: body
        schema:
          type: object
          properties:
            name:
              type: string
            description:
              type: string
    responses:
      200:
        description: Role updated successfully
      404:
        description: Role not found
    """
    role = Role.query.get_or_404(role_id)
    data = request.get_json()
    
    if 'name' in data:
        if Role.query.filter_by(name=data['name']).filter(Role.id != role_id).first():
            return jsonify({'error': 'Role name already exists'}), 409
        role.name = data['name']
    
    if 'description' in data:
        role.description = data['description']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Role updated successfully',
        'role': role.to_dict()
    }), 200

@system_bp.route('/system/roles/<int:role_id>', methods=['DELETE'])
@admin_required
def delete_role(role_id):
    """
    Delete a role
    ---
    tags:
      - System
    parameters:
      - name: role_id
        in: path
        required: true
        type: integer
    responses:
      200:
        description: Role deleted successfully
      404:
        description: Role not found
    """
    role = Role.query.get_or_404(role_id)
    db.session.delete(role)
    db.session.commit()
    return jsonify({'message': 'Role deleted successfully'}), 200

@system_bp.route('/system/permissions', methods=['GET'])
@jwt_required()
def get_permissions():
    """
    Get all permissions
    ---
    tags:
      - System
    responses:
      200:
        description: List of permissions
    """
    permissions = Permission.query.all()
    return jsonify([permission.to_dict() for permission in permissions])

@system_bp.route('/system/logs', methods=['GET'])
@jwt_required()
def get_operation_logs():
    """
    Get operation logs
    ---
    tags:
      - System
    parameters:
      - name: page
        in: query
        type: integer
        default: 1
      - name: per_page
        in: query
        type: integer
        default: 20
      - name: user_id
        in: query
        type: integer
      - name: action
        in: query
        type: string
    responses:
      200:
        description: List of operation logs
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    user_id = request.args.get('user_id')
    action = request.args.get('action')
    
    query = OperationLog.query
    
    if user_id:
        query = query.filter(OperationLog.user_id == user_id)
    
    if action:
        query = query.filter(OperationLog.action == action)
    
    pagination = query.order_by(OperationLog.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return paginate_response(pagination)

@system_bp.route('/system/logs/<int:log_id>', methods=['GET'])
@jwt_required()
def get_operation_log(log_id):
    """
    Get a specific operation log
    ---
    tags:
      - System
    parameters:
      - name: log_id
        in: path
        required: true
        type: integer
    responses:
      200:
        description: Operation log details
      404:
        description: Operation log not found
    """
    log = OperationLog.query.get_or_404(log_id)
    return jsonify(log.to_dict())

@system_bp.route('/system/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    ---
    tags:
      - System
    responses:
      200:
        description: System health status
    """
    # 检查数据库连接
    try:
        db.session.execute('SELECT 1')
        db_status = 'healthy'
    except:
        db_status = 'unhealthy'
    
    return jsonify({
        'status': 'healthy',
        'database': db_status
    })
