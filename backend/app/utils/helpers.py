from flask import jsonify

def paginate_response(pagination, include_counts=True):
    """Create standardized pagination response"""
    return jsonify({
        'items': [item.to_dict(include_counts=include_counts) for item in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'page': pagination.page,
        'per_page': pagination.per_page,
        'has_next': pagination.has_next,
        'has_prev': pagination.has_prev
    })

def success_response(data=None, message='Success'):
    """Create standardized success response"""
    response = {
        'success': True,
        'message': message
    }
    if data is not None:
        response['data'] = data
    return jsonify(response)

def error_response(message='Error', code=400, errors=None):
    """Create standardized error response"""
    response = {
        'success': False,
        'message': message,
        'code': code
    }
    if errors is not None:
        response['errors'] = errors
    return jsonify(response), code
