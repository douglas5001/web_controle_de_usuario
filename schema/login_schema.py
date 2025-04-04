from app import ma
from model.user_model import User
from marshmallow import fields

class LoginSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        fields = ("id", "name", "email", "password")

    name = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.String(required=True)