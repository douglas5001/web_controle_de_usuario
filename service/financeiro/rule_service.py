from app import db
from model.financeiro.rule_model import Rule, RuleFilter

def montar_filtro(rule):
    condicoes = []
    for filtro in rule.filters:
        condicao = f"{filtro.column_name} {filtro.operator} '{filtro.value}'"
        condicoes.append(condicao)
    return " AND ".join(condicoes)


def safe_eval_expression(expr, context):
    # Ambiente limitado para avaliação
    allowed_names = {k: context.get(k, 0) for k in context}
    # Desabilita builtins
    return eval(expr, {"__builtins__": {}}, allowed_names)

def listar_regras(pagina, por_pagina, busca=None, campo_busca="name"):
    consulta = Rule.query
    if busca:
        padrao_busca = f"%{busca}%"
        if campo_busca == "name":
            consulta = consulta.filter(Rule.name.ilike(padrao_busca))
        elif campo_busca == "description":
            consulta = consulta.filter(Rule.description.ilike(padrao_busca))
    return consulta.order_by(Rule.id).paginate(page=pagina, per_page=por_pagina, error_out=False)

def create_rule(data, filters_data):
    new_rule = Rule(
    name=data['name'],
    description=data.get('description'),
    contract=data.get('contract'),
    obs=data.get('obs'),
    verba=data.get('verba'),
    data_financeiro=data.get('data_financeiro'),
    valor_base=data.get('valor_base'),
    valor_liquido=data.get('valor_liquido'),
    descricao_extra=data.get('descricao_extra'),
    plano_de_contas=data.get('plano_de_contas')
    )
    db.session.add(new_rule)
    db.session.flush()  # Para gerar o ID da nova regra

    for f in filters_data:
        new_filter = RuleFilter(
            rule_id=new_rule.id,
            column_name=f['column_name'],
            operator=f['operator'],
            value=f['value']
        )
        db.session.add(new_filter)
    db.session.commit()
    return new_rule

def update_rule(rule, data, filters_data):
    rule.name = data['name']
    rule.description = data.get('description')
    rule.contract = data.get('contract')
    rule.obs = data.get('obs')
    rule.verba = data.get('verba')
    rule.data_financeiro = data.get('data_financeiro')
    rule.valor_base = data.get('valor_base')
    rule.valor_liquido = data.get('valor_liquido')
    rule.descricao_extra = data.get('descricao_extra')
    rule.plano_de_contas = data.get('plano_de_contas')
    
    rule.filters.clear()
    for f in filters_data:
        new_filter = RuleFilter(
            rule_id=rule.id,
            column_name=f['column_name'],
            operator=f['operator'],
            value=f['value']
        )
        rule.filters.append(new_filter)
    db.session.commit()
    return rule

def delete_rule(rule):
    db.session.delete(rule)
    db.session.commit()
