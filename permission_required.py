from functools import wraps
from flask import make_response, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from service.user_service import list_user_id
from service.permission_service import user_has_permission

def permission_required(route_name):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user = list_user_id(user_id)
            if not user or not user_has_permission(user, route_name):
                return make_response(jsonify(message="Você não tem permissão para acessar esta rota"), 403)
            return fn(*args, **kwargs)
        return wrapper
    return decorator
