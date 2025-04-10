import json
import logging
from flask import Blueprint, render_template, request
from sqlalchemy import text
from app import db
from queries.regras_financeiro import query_rules, query_filtro_bradesco
from service.financeiro.rule_service import montar_filtro

logging.basicConfig(level=logging.DEBUG)

relatorio_financeiro_pb = Blueprint("relatorio_financeiro", __name__)

def montar_filtro(filtros: dict) -> str:
    condicoes = []
    for coluna, condicao in filtros.items():
        operador = condicao.get("operator")
        valor = condicao.get("value")
        # Se o valor estiver presente e for numérico, não coloca aspas; senão, coloca aspas
        if valor and valor.isdigit():
            condicao_sql = f"{coluna} {operador} {valor}"
        else:
            condicao_sql = f"{coluna} {operador} '{valor}'"
        condicoes.append(condicao_sql)
    return " AND " + " AND ".join(condicoes) if condicoes else ""

@relatorio_financeiro_pb.route("/relatorio_financeiro", methods=["GET"])
def get_relatorio():
    regra_selecionada_id = request.args.get("regra_id")
    contrato_filtro = request.args.get("contract")

    logging.debug("Parâmetros recebidos - regra_id: %s, contract: %s", regra_selecionada_id, contrato_filtro)

    # Consulta todas as regras
    sql_regras = text(query_rules())
    resultado_regras = db.session.execute(sql_regras)
    todas_regras = [dict(row._mapping) for row in resultado_regras]

    logging.debug("Regras obtidas: %s", todas_regras)

    # Converte os filtros se forem strings JSON
    for regra in todas_regras:
        filtros = regra.get("filtros")
        if isinstance(filtros, str) and filtros:
            try:
                regra["filtros"] = json.loads(filtros)
            except Exception as e:
                logging.exception("Erro ao converter filtros para a regra id %s: %s", regra.get("id"), e)
                regra["filtros"] = {}

    # Filtra as regras para o dropdown com base no contrato (se informado)
    if contrato_filtro:
        regras_filtradas = [r for r in todas_regras if r.get("contract") == contrato_filtro]
    else:
        regras_filtradas = todas_regras

    pastas = []
    regra_atual = None

    if regra_selecionada_id and regra_selecionada_id.isdigit():
        # Caso o usuário tenha selecionado uma regra específica, utiliza-a
        regra_id = int(regra_selecionada_id)
        regra_atual = next((r for r in todas_regras if r.get("id") == regra_id), None)
        if regra_atual:
            filtro_sql = montar_filtro(regra_atual.get("filtros", {}))
            query_final = query_filtro_bradesco(filtro_sql)
            logging.debug("Consulta gerada (regra %s): %s", regra_id, query_final)
            resultado_pastas = db.session.execute(text(query_final))
            pastas = [dict(row._mapping) for row in resultado_pastas]
        else:
            logging.debug("Regra com id %s não encontrada.", regra_selecionada_id)
    elif contrato_filtro:
        # Caso não haja regra específica, mas haja filtro por contrato,
        # executa uma consulta para cada regra que pertença ao contrato
        regras_por_contrato = [r for r in todas_regras if r.get("contract") == contrato_filtro]
        logging.debug("Regras para contrato %s: %s", contrato_filtro, regras_por_contrato)
        for regra in regras_por_contrato:
            filtro_sql = montar_filtro(regra.get("filtros", {}))
            query_final = query_filtro_bradesco(filtro_sql)
            logging.debug("Consulta gerada (regra %s): %s", regra.get("id"), query_final)
            resultado_pastas = db.session.execute(text(query_final))
            pastas += [dict(row._mapping) for row in resultado_pastas]
    else:
        logging.debug("Nenhuma regra ou contrato selecionado; nenhuma consulta executada.")

    todos_contratos = list({r.get('contract') for r in todas_regras if r.get('contract')})

    return render_template(
        "financeiro/relatorio_financeiro.html",
        pastas=pastas,
        regras=regras_filtradas,
        todos_contratos=todos_contratos,
        regra_selecionada_id=int(regra_selecionada_id) if regra_selecionada_id and regra_selecionada_id.isdigit() else None,
        contrato_filtro=contrato_filtro,
        regra_atual=regra_atual
    )
