import os
from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_identity
from config.settings import Config

db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()
api = Api()

def create_app():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    template_dir = os.path.join(base_dir, '..', 'templates')
    static_dir = os.path.join(base_dir, '..', 'static')

    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.config.from_object(Config)

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    api.init_app(app)

    @app.context_processor
    def inject_current_user():
        try:
            from service.user.user_service import list_user_id
            from service.user.permission_service import user_has_permission

            verify_jwt_in_request(optional=True)
            user_id = get_jwt_identity()

            if user_id:
                g.current_user = list_user_id(user_id)

                def has_permission(route_name):
                    return user_has_permission(g.current_user, route_name)

                return {
                    "current_user": g.current_user,
                    "has_permission": has_permission
                }

        except Exception as e:
            print("Erro no context_processor:", e)

        return {
            "current_user": None,
            "has_permission": lambda route: False
        }

    from routes import register_routes
    register_routes(app)

    return app
