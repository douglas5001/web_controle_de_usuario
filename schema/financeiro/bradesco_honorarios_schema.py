# model/bradesco_honorarios_model.py
from app import db

class BradescoHonorario(db.Model):
    __tablename__ = 'bradesco_honorarios'
    __table_args__ = {'schema': 'financeiro'}

    id = db.Column(db.Integer, primary_key=True)
    campo = db.Column(db.String(50), nullable=False)  # pode ser usado para indicar o nome do campo, ex.: "encerramento"
    valor = db.Column(db.Float, nullable=False) 