from flask import Blueprint, render_template, request, redirect, url_for, flash
from service.financeiro.rule_service import create_rule, listar_regras, update_rule, delete_rule
from model.financeiro.rule_model import Rule
from model.financeiro.bradesco_honorarios_model import BradescoHonorario
from sqlalchemy.exc import SQLAlchemyError
import json

rule_bp = Blueprint("rule", __name__, url_prefix="/rules")

@rule_bp.route("/", methods=["GET"])
def get_rules():
    pagina = request.args.get("page", 1, type=int)
    busca = request.args.get("search", "")
    campo_busca = request.args.get("field", "name")
    por_pagina = 10
    regras_paginadas = listar_regras(pagina, por_pagina, busca, campo_busca)
    return render_template(
        "financeiro/rules/list_rules.html",
        rules=regras_paginadas.items,
        pagina=pagina,
        total_paginas=regras_paginadas.pages,
        busca=busca,
        campo_busca=campo_busca
    )

@rule_bp.route("/new", methods=["GET", "POST"])
def new_rule():
    honorarios = BradescoHonorario.query.all()
    if request.method == "POST":
        nome = request.form.get("name")
        descricao = request.form.get("description")
        contract = request.form.get("contract")
        obs = request.form.get("obs")
        verba = request.form.get("verba")
        data_financeiro = request.form.get("data_financeiro")
        # Captura o valor base a partir do tipo selecionado:
        valor_base = request.form.get("valor_base")
        # Mesma lógica para valor_liquido
        valor_liquido = request.form.get("valor_liquido")
        descricao_extra = request.form.get("descricao_extra")
        plano_de_contas = request.form.get("plano_de_contas")
        filtros = json.loads(request.form.get("filters"))
        
        rule_data = {
            "name": nome,
            "description": descricao,
            "contract": contract,
            "obs": obs,
            "verba": verba,
            "data_financeiro": data_financeiro,
            "valor_base": valor_base,
            "valor_liquido": valor_liquido,
            "descricao_extra": descricao_extra,
            "plano_de_contas": plano_de_contas
        }
        
        try:
            create_rule(rule_data, filtros)
            return redirect(url_for("rule.get_rules"))
        except SQLAlchemyError:
            flash("Erro ao criar a regra")
    return render_template("financeiro/rules/new_rule.html", honorarios=honorarios)

@rule_bp.route("/<int:rule_id>/edit", methods=["GET", "POST"])
def edit_rule(rule_id):
    regra = Rule.query.get_or_404(rule_id)
    honorarios = BradescoHonorario.query.all()
    if request.method == "POST":
        nome = request.form.get("name")
        descricao = request.form.get("description")
        contract = request.form.get("contract")
        obs = request.form.get("obs")
        verba = request.form.get("verba")
        data_financeiro = request.form.get("data_financeiro")
        valor_base_tipo = request.form.get("valor_base_tipo")
        if valor_base_tipo == "expressao":
            valor_base = request.form.get("valor_base_expressao")
        else:
            valor_base = request.form.get("valor_base")
        valor_liquido_tipo = request.form.get("valor_liquido_tipo")
        if valor_liquido_tipo == "expressao":
            valor_liquido = request.form.get("valor_liquido_expressao")
        else:
            valor_liquido = request.form.get("valor_liquido")
        descricao_extra = request.form.get("descricao_extra")
        plano_de_contas = request.form.get("plano_de_contas")
        filtros = json.loads(request.form.get("filters"))
        
        rule_data = {
            "name": nome,
            "description": descricao,
            "contract": contract,
            "obs": obs,
            "verba": verba,
            "data_financeiro": data_financeiro,
            "valor_base": valor_base,
            "valor_base_tipo": valor_base_tipo,
            "valor_liquido": valor_liquido,
            "valor_liquido_tipo": valor_liquido_tipo,
            "descricao_extra": descricao_extra,
            "plano_de_contas": plano_de_contas
        }
        
        try:
            update_rule(regra, rule_data, filtros)
            return redirect(url_for("rule.get_rules"))
        except SQLAlchemyError:
            flash("Erro ao atualizar a regra")
    return render_template("financeiro/rules/edit_rule.html", rule=regra, honorarios=honorarios)

@rule_bp.route("/<int:rule_id>/delete", methods=["POST"])
def remove_rule(rule_id):
    regra = Rule.query.get_or_404(rule_id)
    try:
        delete_rule(regra)
        flash("Regra removida com sucesso")
    except SQLAlchemyError:
        flash("Erro ao remover a regra")
    return redirect(url_for("rule.get_rules"))
