from flask import Blueprint, render_template, request, redirect, url_for, make_response
from flask_jwt_extended import create_access_token, get_jwt_identity, verify_jwt_in_request
from app import jwt
from service.user_service import list_user_email, list_user_id
from flask import g
auth_bp = Blueprint("auth", __name__)

@auth_bp.context_processor
def inject_current_user():
    try:
        verify_jwt_in_request(optional=True)  # Verifica se há JWT (token) sem exigir obrigatoriamente
        user_id = get_jwt_identity()
        if user_id:
            g.current_user = list_user_id(user_id)
            return {"current_user": g.current_user}
    except:
        pass

    return {"current_user": None}

def add_claims_to_access_token(identity):
    user_token = list_user_id(identity)
    return {'roles': 'admin' if user_token.is_admin else 'user'}

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("user/login.html")

    email = request.form.get("email")
    password = request.form.get("password")

    user = list_user_email(email)
    if user and user.show_password(password):
        access_token = create_access_token(identity=str(user.id), additional_claims=add_claims_to_access_token(user.id))
        response = make_response(redirect("/"))
        response.set_cookie("access_token_cookie", access_token, httponly=True)
        return response

    return render_template("user/login.html", error="Credenciais inválidas")
