import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api
from flask_jwt_extended import JWTManager
from config.settings import Config

db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()
api = Api()

def create_app():
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    TEMPLATE_DIR = os.path.join(BASE_DIR, '..', 'templates')
    STATIC_DIR = os.path.join(BASE_DIR, '..', 'static')

    app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
    
    from config.settings import Config
    app.config.from_object(Config)

    from app import db, ma, jwt, api
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    api.init_app(app)

    from routes import register_routes
    register_routes(app)

    return app
