from app import db
from datetime import datetime

class Rule(db.Model):
    __tablename__ = 'rule'
    __table_args__ = {'schema': 'financeiro'}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    contract = db.Column(db.String(100))
    obs = db.Column(db.Text)
    verba = db.Column(db.String(100))
    data_financeiro = db.Column(db.String(50))
    valor_base = db.Column(db.String(100))  # Se tipo==campo, armazena o nome do campo; se expressao, armazena a expressão
    valor_liquido = db.Column(db.String(100))
    descricao_extra = db.Column(db.String(255))
    plano_de_contas = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    filters = db.relationship('RuleFilter', backref='rule', cascade='all, delete-orphan')

class RuleFilter(db.Model):
    __tablename__ = 'rule_filter'
    __table_args__ = {'schema': 'financeiro'}
    id = db.Column(db.Integer, primary_key=True)
    rule_id = db.Column(db.Integer, db.ForeignKey('financeiro.rule.id'), nullable=False)
    column_name = db.Column(db.String(100), nullable=False)
    operator = db.Column(db.String(50), nullable=False)
    value = db.Column(db.String(255), nullable=False)
    

