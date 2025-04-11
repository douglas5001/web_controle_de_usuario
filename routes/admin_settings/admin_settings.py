from flask import Blueprint, render_template

from permission_required import permission_required

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin_settings", methods=["GET"])
@permission_required("admin")
def admin_settings():
    pass

    return render_template("user/admin_settings.html")


@admin_bp.route("/profile", methods=["GET"])
@permission_required("admin")
def profile():
    return render_template("user/profile.html")