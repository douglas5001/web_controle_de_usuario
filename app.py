from flask import Flask, request, make_response, jsonify, url_for, redirect, render_template
from __init__ import db, ma, jwt
from flask_restful import Api, Resource
from decorator import admin_required
from schema.login_schema import LoginSchema
from schema.user_schema import UserSchema
from entity.user import User
from service.user_service import list_user, create_user, delete_user, list_user_id, update_user, list_user_email
import os
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, decode_token, get_jwt_identity, jwt_required
from datetime import timedelta
import logging

load_dotenv()
logging.basicConfig(level=logging.DEBUG)


server = os.getenv('server')
database = os.getenv('database')
username = os.getenv('username')
password = os.getenv('password')

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql+psycopg2://{username}:{password}@{server}/{database}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

api = Api(app)
db.init_app(app)
ma.init_app(app)
jwt.init_app(app)

# Configurações do JWT
app.config["JWT_SECRET_KEY"] = "sua_chave_muito_secreta"
app.config["JWT_COOKIE_SECURE"] = False  # Apenas use False em ambiente de desenvolvimento
app.config["JWT_COOKIE_HTTPONLY"] = True
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_CSRF_PROTECT"] = False

jwt = JWTManager(app)


@app.route("/register_task", methods=["GET", "POST"])
@jwt_required()  # Exige autenticação
def register_task():
    user_id = get_jwt_identity()  # Obtém o ID do usuário autenticado
    if request.method == "POST":
        ts = TaskSchema()
        validate = ts.validate(request.form)
        if validate:
            return render_template("register_task.html", errors=validate)

        event = request.form["event"]
        content = request.form["content"]
        priority = request.form["priority"]
        date_creation = request.form["date_creation"]

        new_task = Task(event=event, content=content, priority=int(priority), date_creation=date_creation)
        user = list_user_id(user_id)

        if user:
            user.tasks.append(new_task)  # Associa a tarefa ao usuário autenticado
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")  # Redireciona para a página inicial ou outra página

    return render_template("register_task.html")


def add_claims_to_access_token(identity):
    user_token = list_user_id(identity)
    if user_token.is_admin:
        roles = 'admin'
    else:
        roles = 'user'
    return {'roles':roles}

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email")
    password = request.form.get("password")

    user = list_user_email(email)
    if user and user.show_password(password):
        access_token = create_access_token(identity=str(user.id), additional_claims=add_claims_to_access_token(user.id))
        app.logger.info(access_token)
        response = make_response(redirect("/"))
        response.set_cookie("access_token_cookie", access_token, httponly=True)
        return response
    else:
        return render_template("login.html", error="Credenciais inválidas")


@app.route("/users", methods=["GET"])
@jwt_required()  # Valida o token armazenado no cookie
def get_user():
    user_id = get_jwt_identity()
    app.logger.info(f"user_id ==>> {user_id}")
    user_model = list_user()
    user_schema = UserSchema(many=True)
    users = user_schema.dump(user_model)

    return render_template("users.html", users=users)



@app.route("/register", methods=["GET", "POST"])
#@admin_required
def register_user():
    if request.method == "POST":
        us = UserSchema()
        validate = us.validate(request.form)
        if validate:
            return render_template("register.html", errors=validate)

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        is_admin = request.form["is_admin"]
        app.logger.info(is_admin)
        is_admin = is_admin.lower() == "true"
        new_user = User(name=name, email=email, password=password, is_admin=is_admin)
        result = create_user(new_user)
        if result:
            return redirect(url_for("get_user"))  
    return render_template("register.html")

@app.route("/<int:id>/remove_user")
def remove_user(id):
    delete_user(id)
    return redirect(url_for('get_user'))

@app.route("/<int:id>/update_user", methods=["GET", "POST"])
def put_user(id):
    user_db = list_user_id(id)
    if user_db is None:
        return make_response(jsonify("Usuário não encontrado"), 404)
    
    us = UserSchema()

    if request.method == "GET":
        return render_template("update_user.html", user=user_db)

    validate = us.validate(request.form)
    if validate:
        return make_response(jsonify(validate), 400)
    else:
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        is_admin = request.form["is_admin"]
        
        new_user = User(name=name, email=email, password=password, is_admin=is_admin)
        update_user(user_db, new_user)
        
        #user_new = list_user_id(id)
        return redirect("/users")

@app.route("/")
def layout():
    return render_template("index.html")



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)