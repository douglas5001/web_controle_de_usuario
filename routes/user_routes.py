from flask import Blueprint, render_template, redirect, request, url_for, jsonify, make_response
from schema.user_schema import UserSchema
from service.user_service import list_user, create_user, delete_user, list_user_id, update_user
from service.profile_service import list_profiles, get_profile_by_id
from permission_required import permission_required
from model.user_model import User

user_bp = Blueprint("user", __name__)

@user_bp.route("/users")
@permission_required("rota_listar_usuarios")
def get_user():
    users = list_user()
    users_data = UserSchema(many=True).dump(users)
    return render_template("user/users.html", users=users_data)

@user_bp.route("/register", methods=["GET", "POST"])
def register_user():
    if request.method == "POST":
        profile_id_str = request.form.get("profile_id")
        if profile_id_str == "":
            profile_id_str = None

        data = {
            "name": request.form.get("name"),
            "email": request.form.get("email"),
            "password": request.form.get("password"),
            "is_admin": request.form.get("is_admin"),
            "profile_id": profile_id_str
        }
        us = UserSchema()
        errors = us.validate(data)
        if errors:
            profiles = list_profiles()
            return render_template("user/register.html", errors=errors, profiles=profiles)

        new_user = User(
            name=data["name"],
            email=data["email"],
            password=data["password"],
            is_admin=(data["is_admin"].lower() == "true"),
            profile_id=int(data["profile_id"]) if data["profile_id"] else None
        )
        create_user(new_user)
        return redirect(url_for("user.get_user"))

    profiles = list_profiles()
    return render_template("user/register.html", profiles=profiles)

@user_bp.route("/<int:id>/remove_user")
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
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]
    is_admin = request.form["is_admin"].lower() == "true"
    profile_id = request.form.get("profile_id")
    new_user = User(
        name=name,
        email=email,
        password=password,
        is_admin=is_admin,
        profile_id=int(profile_id) if profile_id else None
    )
    update_user(user_db, new_user)
    return redirect(url_for("user.get_user"))
