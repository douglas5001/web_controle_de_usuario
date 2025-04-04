

# from io import BytesIO
# from flask import send_file
# import pandas as pd
# from sqlalchemy import text
# from app import db
# from queries.notificacoes import import_notioficacoes_civel


# @app.route("/notificacoes/exportar")
# def exportar_notificacoes_excel():
#     sql = text(import_notioficacoes_civel())
#     resultado = db.session.execute(sql)
#     pastas = [dict(row._mapping) for row in resultado]

#     if not pastas:
#         return "Nenhuma notificação encontrada.", 404

#     df = pd.DataFrame(pastas)

#     output = BytesIO()
#     with pd.ExcelWriter(output, engine='openpyxl') as writer:
#         df.to_excel(writer, index=False, sheet_name="Notificações")

#     output.seek(0)

#     return send_file(
#         output,
#         as_attachment=True,
#         download_name="notificacoes_civeis.xlsx",
#         mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#     )