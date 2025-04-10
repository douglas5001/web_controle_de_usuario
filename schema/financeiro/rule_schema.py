from app import ma
from model.financeiro.rule_model import Rule, RuleFilter
from marshmallow import fields

class RuleFilterSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RuleFilter
        load_instance = True
        include_fk = True

class RuleSchema(ma.SQLAlchemyAutoSchema):
    filters = fields.List(fields.Nested(RuleFilterSchema))
    class Meta:
        model = Rule
        load_instance = True
        include_relationships = True
        fields = (
            "id", "name", "description", "contract", "obs", "verba", "data_financeiro", 
            "valor_base" "valor_liquido",
            "descricao_extra", "plano_de_contas", "filters"
        )
