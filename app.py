from flask import Flask, request, make_response, jsonify, url_for, redirect, render_template
from __init__ import db, ma
from flask_restful import Api
from schema.user_schema import UserSchema
from entity.user import User
from service.user_service import list_user, create_user, delete_user
import os
from dotenv import load_dotenv

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

@app.route("/")
def get_user():
    user_model = list_user()
    user_schema = UserSchema(many=True)
    users = user_schema.dump(user_model)
    return render_template("index.html", users=users)

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
    

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
