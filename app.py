from flask import Flask, request, make_response, jsonify, url_for, redirect, render_template
from __init__ import db, ma, jwt
from flask_restful import Api, Resource
from schema.login_schema import LoginSchema
from schema.user_schema import UserSchema
from entity.user import User
from service.user_service import list_user, create_user, delete_user, list_user_id, update_user, list_user_email
import os
from dotenv import load_dotenv
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from datetime import timedelta

load_dotenv()

server = os.getenv('host')
database = os.getenv('database')
username = os.getenv('user')
password = os.getenv('password')

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql+psycopg2://{username}:{password}@{server}/{database}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

api = Api(app)
db.init_app(app)
ma.init_app(app)
jwt.init_app(app)

app.config["JWT_SECRET_KEY"] = "sua_chave_muito_secreta"

@app.route("/", methods=["GET"])
@jwt_required(locations=["cookies"])  # Busca o token nos cookies
def get_user():
    current_user_id = get_jwt_identity()
    user_model = list_user_id(current_user_id)

    if not user_model:
        return jsonify({"message": "Usuário não encontrado"}), 404
    
    user_schema = UserSchema()
    user_data = user_schema.dump(user_model)
    return render_template("index.html", user=user_data)

@app.route("/register", methods=["GET", "POST"])
def register_user():
    if request.method == "POST":
        us = UserSchema()
        validate = us.validate(request.form)
        if validate:
            return render_template("register.html", errors=validate)

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        new_user = User(name=name, email=email, password=password)
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
        
        new_user = User(name=name, email=email, password=password)
        update_user(user_db, new_user)
        
        #user_new = list_user_id(id)
        return redirect("/")
   
def add_claims_to_access_token(identity):
    user_token = list_user_id(identity)
    if user_token.is_admin:
        roles = 'admin'
    else:
        roles = 'user'
    return {'roles':roles}

@app.route("/login", methods=["GET", "POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    user = list_user_email(email)
    if user and user.show_password(password):
        # Gerar token JWT
        access_token = create_access_token(identity=user.id)

        # Retornar o token em um cookie
        response = make_response(redirect("/"))  # Redireciona para a rota protegida
        response.set_cookie("access_token", access_token, httponly=True, secure=True)
        return response
    else:
        return render_template("login.html", error="Credenciais inválidas")




if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)