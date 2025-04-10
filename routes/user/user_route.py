import csv
import io
from flask import Blueprint, render_template, redirect, request, url_for, jsonify, make_response
from permission_required import permission_required
from schema.user.user_schema import UserSchema
from service.user.user_service import (
    list_user,
    create_user,
    delete_user,
    list_user_id,
    update_user,
)
from service.user.profile_service import list_profiles
from model.user_model import User

user_bp = Blueprint("user", __name__)


@user_bp.route("/users")
@permission_required("admin")
def get_user():
    page   = request.args.get("page", 1, type=int)
    search = request.args.get("search", "")
    field  = request.args.get("field", "name")
    per_page = 10

    users_paginated = list_user(page, per_page, search, field)

    # ➜ não serialize
    users = users_paginated.items
    profiles = list_profiles()

    return render_template(
        "user/users.html",
        users=users,
        profiles=profiles,
        search=search,
        field=field,
        page=page,
        total_pages=users_paginated.pages,
    )


@user_bp.route("/register", methods=["POST"])
@permission_required("admin")
def register_user():
    profile_id_str = request.form.get("profile_id") or None
    file_storage = request.files.get("avatar")

    data = {
        "name": request.form.get("name"),
        "email": request.form.get("email"),
        "password": request.form.get("password"),
        "is_admin": request.form.get("is_admin"),
        "profile_id": profile_id_str,
    }

    # Validação dos dados do formulário
    errors = UserSchema().validate(data)
    if errors:
        profiles = list_profiles()
        return render_template("user/users.html", errors=errors, profiles=profiles)

    # Se a imagem não for permitida, retornará um erro
    try:
        new_user = User(
            name=data["name"],
            email=data["email"],
            password=data["password"],
            is_admin=data["is_admin"].lower() == "true",
            profile_id=int(data["profile_id"]) if data["profile_id"] else None,
        )

        # Chama o serviço para criar o usuário e processar o avatar
        create_user(new_user, file_storage)
    except ValueError as e:
        aviso = str(e)  # O erro gerado em save_avatar() como "Extensão de imagem não permitida"
        return redirect(url_for("user.get_user", aviso=aviso))

    return redirect(url_for("user.get_user"))


@user_bp.route("/<int:id>/remove_user")
@permission_required("admin")
def remove_user(id):
    delete_user(id)
    return redirect(url_for("user.get_user"))


@user_bp.route("/<int:id>/update_user", methods=["GET", "POST"])
def put_user(id):
    user_db = list_user_id(id)
    if not user_db:
        return make_response(jsonify("Usuário não encontrado"), 404)

    if request.method == "GET":
        profiles = list_profiles()
        return render_template("user/update_user.html", user=user_db, profiles=profiles)

    try:
        name = request.form.get("name")
        email = request.form.get("email")
        is_admin = request.form.get("is_admin", "false").lower() == "true"
        profile_id_str = request.form.get("profile_id")
        profile_id = int(profile_id_str) if profile_id_str else None

        change_pwd = request.form.get("change_password") == "on"
        remove_avatar = request.form.get("remove_avatar") == "true"
        file_storage = request.files.get("avatar")

        password = request.form.get("password", "")

        new_user = User(
            name=name,
            email=email,
            password=password,
            is_admin=is_admin,
            profile_id=profile_id
        )

        update_user(user_db, new_user, file_storage, remove_avatar, change_pwd)
        return redirect(url_for("user.get_user"))

    except ValueError as e:
        aviso = str(e)
        return redirect(url_for("user.get_user", aviso=aviso))


@user_bp.route("/users/excel")
@permission_required("admin")
def users_excel():
    page = request.args.get("page", 1, type=int)
    search = request.args.get("search", "")
    per_page = 999_999

    users_paginated = list_user(page, per_page, search)
    output = io.StringIO()
    writer = csv.writer(output, delimiter=";")
    writer.writerow(["ID", "Nome", "Email", "Admin", "Perfil"])

    for u in users_paginated.items:
        perfil = u.profile.name if u.profile else "Sem Perfil"
        writer.writerow([u.id, u.name, u.email, "Sim" if u.is_admin else "Não", perfil])

    output.seek(0)
    response = make_response(output.read())
    response.headers["Content-Disposition"] = "attachment; filename=usuarios.csv"
    response.headers["Content-type"] = "text/csv"
    return response
