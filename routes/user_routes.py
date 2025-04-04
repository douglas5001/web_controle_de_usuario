from flask import Blueprint, render_template, redirect, request, url_for, jsonify, make_response
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from schema.user_schema import UserSchema
from service.user_service import list_user, create_user, delete_user, list_user_id, update_user
from entity.user import User

user_bp = Blueprint("user", __name__)

@user_bp.route("/users")
@jwt_required()
def get_user():
    user_model = list_user()
    users = UserSchema(many=True).dump(user_model)
    return render_template("users.html", users=users)

@user_bp.route("/register", methods=["GET", "POST"])
def register_user():
    if request.method == "POST":
        us = UserSchema()
        validate = us.validate(request.form)
        if validate:
            return render_template("register.html", errors=validate)

        user = User(
            name=request.form["name"],
            email=request.form["email"],
            password=request.form["password"],
            is_admin=request.form["is_admin"].lower() == "true"
        )
        create_user(user)
        return redirect(url_for("user.get_user"))

    return render_template("register.html")

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
        return render_template("update_user.html", user=user_db)

    new_user = User(
        name=request.form["name"],
        email=request.form["email"],
        password=request.form["password"],
        is_admin=request.form["is_admin"].lower() == "true"
    )
    update_user(user_db, new_user)
    return redirect(url_for("user.get_user"))
