from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
from app import db
from app.models.user import User, Role, Permission
from app.utils.decorators import admin_required, permission_required
from app.utils.helpers import paginate_response
from app.utils.cache import get_redis

auth_bp = Blueprint('auth', __name__)

LOGIN_MAX_ATTEMPTS = 5
LOGIN_LOCKOUT_TIME = 300  # 5 minutes

def check_login_rate_limit(username):
    """Check if user has exceeded login attempts"""
    r = get_redis()
    if r is None:
        return True, None
    
    key = f"login_failed:{username}"
    attempts = r.get(key)
    
    if attempts and int(attempts) >= LOGIN_MAX_ATTEMPTS:
        ttl = r.ttl(key)
        return False, f"登录尝试过多，请{int(ttl) if ttl > 0 else LOGIN_LOCKOUT_TIME}秒后重试"
    
    return True, None

def record_login_failure(username):
    """Record failed login attempt"""
    r = get_redis()
    if r is None:
        return
    
    key = f"login_failed:{username}"
    try:
        r.incr(key)
        r.expire(key, LOGIN_LOCKOUT_TIME)
    except Exception:
        pass

def clear_login_failures(username):
    """Clear failed login attempts on successful login"""
    r = get_redis()
    if r is None:
        return
    
    key = f"login_failed:{username}"
    try:
        r.delete(key)
    except Exception:
        pass

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    User login
    ---
    tags:
      - Authentication
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
            password:
              type: string
    responses:
      200:
        description: Login successful
      401:
        description: Invalid credentials
      429:
        description: Too many login attempts
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Missing username or password'}), 400
    
    allowed, error_msg = check_login_rate_limit(username)
    if not allowed:
        return jsonify({'error': error_msg}), 429
    
    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password_hash, password):
        record_login_failure(username)
        return jsonify({'error': 'Invalid credentials'}), 401
    
    clear_login_failures(username)
    access_token = create_access_token(identity=user.id)
    return jsonify({
        'access_token': access_token,
        'user': user.to_dict()
    }), 200

@auth_bp.route('/register', methods=['POST'])
@admin_required
def register():
    """
    Register a new user
    ---
    tags:
      - Authentication
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
      409:
        description: User already exists
    """
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role_id = data.get('role_id', 2)
    
    if not username or not email or not password:
        return jsonify({'error': 'Missing required fields'}), 400
    
    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({'error': 'User already exists'}), 409
    
    password_hash = generate_password_hash(password)
    user = User(
        username=username,
        email=email,
        password_hash=password_hash,
        role_id=role_id
    )
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User created successfully', 'user': user.to_dict()}), 201

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """
    Get current user profile
    ---
    tags:
      - Authentication
    responses:
      200:
        description: User profile
    """
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """
    Update current user profile
    ---
    tags:
      - Authentication
    parameters:
      - in: body
        name: body
        schema:
          type: object
          properties:
            email:
              type: string
            password:
              type: string
    responses:
      200:
        description: Profile updated
    """
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    if 'email' in data:
        user.email = data['email']
    
    if 'password' in data and data['password']:
        user.password_hash = generate_password_hash(data['password'])
    
    db.session.commit()
    return jsonify({'message': 'Profile updated', 'user': user.to_dict()})
