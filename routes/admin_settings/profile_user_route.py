import csv
import io
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, make_response
from model.permission_model import Permission
from permission_required import permission_required
from schema.user.profile_schema import ProfileSchema
from service.user.permission_service import grant_permission_to_profile
from service.user.profile_service import list_profile_page, create_profile, get_profile_by_id, delete_profile
from service.user.profile_service import update_profile_with_permissions
profile_bp = Blueprint("profile", __name__)


@profile_bp.route("/profile/permissoes-existentes")
@permission_required("admin")
def permissoes_existentes():
    permissoes = Permission.query.with_entities(Permission.route_name).distinct().all()
    return jsonify([p.route_name for p in permissoes])

@profile_bp.route("/permission/autocomplete")
@permission_required("admin")
def autocomplete_permissions():
    permissoes = Permission.query.with_entities(Permission.route_name).distinct().all()
    nomes = [p.route_name for p in permissoes]
    return jsonify(nomes)

@profile_bp.route("/permissions")
@permission_required("admin")
def list_all_permissions():
    permissoes = Permission.query.with_entities(Permission.route_name).distinct().all()
    return jsonify([p.route_name for p in permissoes])

@profile_bp.route("/profile_user")
@permission_required("admin")
def list_profiles_route():
    pagina = request.args.get("page", 1, type=int)
    busca = request.args.get("search", "")
    campo = request.args.get("field", "name")
    por_pagina = 10
    perfis_paginados = list_profile_page(pagina, por_pagina, busca, campo)
    perfis_serializados = ProfileSchema(many=True).dump(perfis_paginados.items)
    return render_template("user/profile_user.html", perfis=perfis_serializados, busca=busca, campo=campo, pagina=pagina, total_paginas=perfis_paginados.pages)

@profile_bp.route("/profile/register", methods=["GET", "POST"])
@permission_required("admin")
def register_profile():
    if request.method == "POST":
        nome = request.form.get("nome")
        permissoes_json = request.form.get("permissoes")

        if not nome:
            return render_template("profile/register_profile.html", erros={"nome": "Nome é obrigatório"})

        perfil = create_profile(nome)

        if permissoes_json:
            import json
            permissoes = json.loads(permissoes_json)
            for p in permissoes:
                grant_permission_to_profile(perfil.id, p)

        return redirect(url_for("profile.list_profiles_route"))

    return render_template("profile/register_profile.html")

@profile_bp.route("/profile/<int:id>/update", methods=["GET", "POST"])
@permission_required("admin")
def update_profile_route(id):
    perfil_bd = get_profile_by_id(id)
    if not perfil_bd:
        return make_response(jsonify("Perfil não encontrado"), 404)

    if request.method == "GET":
        return render_template("profile/update_profile.html", perfil=perfil_bd)

    novo_nome = request.form.get("nome")
    permissoes_json = request.form.get("permissoes")

    import json
    permissoes = json.loads(permissoes_json) if permissoes_json else []

    update_profile_with_permissions(perfil_bd, novo_nome, permissoes)

    return redirect(url_for("profile.list_profiles_route"))

@profile_bp.route("/profile/<int:id>/remove")
@permission_required("admin")
def remove_profile(id):
    delete_profile(id)
    return redirect(url_for("profile.list_profiles_route"))

@profile_bp.route("/profile/excel")
@permission_required("admin")
def export_profiles_excel():
    busca = request.args.get("search", "")
    campo = request.args.get("field", "name")
    por_pagina = 999999
    perfis_paginated = list_profile_page(1, por_pagina, busca, campo)
    output = io.StringIO()
    writer = csv.writer(output, delimiter=';')
    writer.writerow(["ID", "Nome"])
    for perfil in perfis_paginated.items:
        writer.writerow([perfil.id, perfil.name])
    output.seek(0)
    response = make_response(output.read())
    response.headers["Content-Disposition"] = "attachment; filename=perfis.csv"
    response.headers["Content-type"] = "text/csv"
    return response
