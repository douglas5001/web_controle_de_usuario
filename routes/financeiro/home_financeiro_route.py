from flask import Blueprint, render_template

from permission_required import permission_required

home_financeiro_bp = Blueprint("home_financeiro_bp", __name__)


@home_financeiro_bp.route("/gerenciamento-fianceiro", methods=["GET"])
@permission_required("financeiro")
def admin_settings():
    pass

    return render_template("financeiro/home_financeiro.html")

