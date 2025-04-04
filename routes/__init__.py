from .auth_routes import auth_bp
from .user_routes import user_bp
from .home_routes import home_bp
from .notification_gcpj_routes import notification_gcpj_pb
# adicione outros blueprints se quiser

def register_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(notification_gcpj_pb)
