from .user.auth_route import auth_bp
from .user.user_route import user_bp
from .admin_settings.profile_user_route import profile_bp
from .home_route import home_bp
from .admin_settings.admin_settings import admin_bp
from .notification_gcpj_route import notification_gcpj_pb
from .task_route import task_bp

# adicione outros blueprints se quiser

def register_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(notification_gcpj_pb)
    app.register_blueprint(task_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(profile_bp)

