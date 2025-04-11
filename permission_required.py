from flask import make_response, render_template, redirect, url_for
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from functools import wraps
from service.user.user_service import list_user_id
from service.user.permission_service import user_has_permission

def permission_required(route_name):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
            except Exception:
                return redirect(url_for("auth.login", aviso="Faça login para acessar essa página"))  # ou render_template("erros/401.html")

            user_id = get_jwt_identity()
            user = list_user_id(user_id)

            if not user:
                return redirect(url_for("auth.login"))

            if not user_has_permission(user, route_name):
                return make_response(render_template("error/403.html", mensagem="Você não tem permissão para acessar esta rota"), 403)

            return fn(*args, **kwargs)
        return wrapper
    return decorator
