from flask import Blueprint, render_template, redirect, request, url_for, jsonify, make_response
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from decorator import admin_required
from permission_required import permission_required
from schema.user_schema import UserSchema
from service.user_service import list_user, create_user, delete_user, list_user_id, update_user
from entity.user import User

home_bp = Blueprint("home", __name__)

@home_bp.route("/", methods=["GET"])
@permission_required("rota_listar_usuarios")
def layout():
    user_id = get_jwt_identity()  # Obtém o ID do usuário autenticado
    user = list_user_id(user_id)

    if not user:
        return redirect(url_for("login"))

    tasks = user.tasks  # Obtém as tarefas associadas ao usuário logado
    return render_template("index.html", tasks=tasks)
