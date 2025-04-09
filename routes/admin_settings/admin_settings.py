from flask import Blueprint, render_template

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin_settings", methods=["GET"])
def admin_settings():
    pass

    return render_template("user/admin_settings.html")


@admin_bp.route("/profile", methods=["GET"])
def profile():
    return render_template("user/profile.html")