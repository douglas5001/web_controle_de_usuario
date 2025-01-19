from functools import wraps
from flask_jwt_extended import get_jwt, verify_jwt_in_request
from flask import make_response, jsonify

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # Verifica se o token JWT está presente e válido
        verify_jwt_in_request()
        
        # Obtém os claims do token
        claims = get_jwt()
        
        # Verifica se o usuário tem o papel de 'admin'
        if claims.get('roles') != 'admin':
            return make_response(jsonify(message='Não é permitido esse recurso, só para administradores'), 403)
        
        # Chama a função original se o usuário for admin
        return fn(*args, **kwargs)
    
    return wrapper