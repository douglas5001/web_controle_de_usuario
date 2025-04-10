from flask import Blueprint, render_template

home_financeiro_bp = Blueprint("home_financeiro_bp", __name__)


@home_financeiro_bp.route("/home_financeiro", methods=["GET"])
def admin_settings():
    pass

    return render_template("financeiro/home_financeiro.html")

