# models/honorario_model.py
from app import db

class BradescoHonorario(db.Model):
    __tablename__ = "bradesco_honorarios"
    __table_args__ = {"schema": "financeiro"}

    id = db.Column(db.Integer, primary_key=True)
    campo = db.Column(db.String(100), nullable=False)
    valor = db.Column(db.Float, nullable=False)
