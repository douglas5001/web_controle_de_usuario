from flask import Blueprint, render_template, redirect, request, url_for, jsonify, make_response
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from decorator import admin_required
from model.user_model import Task
from permission_required import permission_required
from schema.user.user_schema import UserSchema
from service.user.user_service import list_user, create_user, delete_user, list_user_id, update_user
from entity.user import User



task_bp = Blueprint("task", __name__)


@task_bp.route("/register_task", methods=["GET", "POST"])
@permission_required("todos")  
def register_task():
    user_id = get_jwt_identity() 

    if request.method == "POST":
        event = request.form["event"]
        content = request.form["content"]
        priority = request.form["priority"]
        date_creation = request.form["date_creation"]

        new_task = Task(event=event, content=content, priority=int(priority), date_creation=date_creation)
        user = list_user_id(user_id)

        if user:
            new_task.users.append(user) 
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")

    return render_template("task/register_task.html")