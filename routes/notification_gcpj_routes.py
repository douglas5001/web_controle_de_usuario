import time
from io import BytesIO

import pandas as pd
from app import db
from flask import Blueprint, render_template, send_file
from sqlalchemy import text
from flask_jwt_extended import jwt_required, get_jwt_identity

import plotly.graph_objs as go
from plotly.offline import plot

from queries.notificacoes import import_notioficacoes_civel
import jwt


notification_gcpj_pb = Blueprint("notification_gcpj", __name__)

@notification_gcpj_pb.route("/dashboard")
def dashboard():
    vendas = [
        {"mes": "Janeiro", "quantidade": 10},
        {"mes": "Fevereiro", "quantidade": 15},
        {"mes": "Março", "quantidade": 13},
        {"mes": "Abril", "quantidade": 17}
    ]

    meses = [item["mes"] for item in vendas]
    quantidades = [item["quantidade"] for item in vendas]

    grafico = go.Bar(x=meses, y=quantidades)
    layout = go.Layout(title="Vendas por Mês", xaxis=dict(title="Mês"), yaxis=dict(title="Quantidade"))
    figura = go.Figure(data=[grafico], layout=layout)
    grafico_html = plot(figura, output_type="div", include_plotlyjs=True)

    ########
    METABASE_SITE_URL = "http://metabase.saratt.com.br"
    METABASE_SECRET_KEY = "cfda76a2c906ff51dd438dc5280c77876066db7f6412c92e0874d34cbf20f8f8"
    payload = {
        "resource": {"dashboard": 17},
        "params": {},
        "exp": round(time.time()) + 600
    }

    token = jwt.encode(payload, METABASE_SECRET_KEY, algorithm="HS256")
    iframe_url = f"{METABASE_SITE_URL}/embed/dashboard/{token}#bordered=true&titled=true"

    return render_template("dashboard.html", grafico=grafico_html, iframe_url=iframe_url)


@notification_gcpj_pb.route("/notificacoes")
def notificacoes():
    sql = text(import_notioficacoes_civel())
    resultado = db.session.execute(sql)

    pastas = [dict(row._mapping) for row in resultado]
    
    METABASE_SITE_URL = "http://metabase.saratt.com.br"
    METABASE_SECRET_KEY = "cfda76a2c906ff51dd438dc5280c77876066db7f6412c92e0874d34cbf20f8f8"
    payload = {
        "resource": {"dashboard": 17},
        "params": {},
        "exp": round(time.time()) + 600
    }

    token = jwt.encode(payload, METABASE_SECRET_KEY, algorithm="HS256")
    iframeUrl = METABASE_SITE_URL + "/embed/dashboard/" + token + "#theme=night&background=false&bordered=false&titled=false"

    return render_template("dashboards/notificacoes.html", pastas=pastas, iframe_url=iframeUrl)


@notification_gcpj_pb.route("/relatorio_ti")
def relatorio_ti():
    METABASE_SITE_URL = "http://metabase.saratt.com.br"
    METABASE_SECRET_KEY = "cfda76a2c906ff51dd438dc5280c77876066db7f6412c92e0874d34cbf20f8f8"

    payload = {
    "resource": {"dashboard": 12},
    "params": {
        
    },
    "exp": round(time.time()) + (60 * 10) # 10 minute expiration
    }
    token = jwt.encode(payload, METABASE_SECRET_KEY, algorithm="HS256")

    iframeUrl = METABASE_SITE_URL + "/embed/dashboard/" + token + "#background=false&bordered=false&titled=false"
    
    return render_template("dashboards/relatorio_ti.html", iframe_url=iframeUrl)  
    
    
    
@notification_gcpj_pb.route("/notificacoes/exportar")
def exportar_notificacoes_excel():
    sql = text(import_notioficacoes_civel())
    resultado = db.session.execute(sql)

    pastas = [dict(row._mapping) for row in resultado]

    if not pastas:
        return "Nenhuma notificação encontrada.", 404

    df = pd.DataFrame(pastas)

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name="Notificações")

    output.seek(0)
    return send_file(
        output,
        as_attachment=True,
        download_name="notificacoes_civeis.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )