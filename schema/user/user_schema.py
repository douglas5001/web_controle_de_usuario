from app import ma
from model.user_model import User
from model.user_model import Task       # importa do módulo correto
from marshmallow import fields
from schema.user.profile_schema import ProfileSchema


class TaskSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        load_instance = True
        fields = ("id", "event", "content", "priority", "date_creation")


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        fields = (
            "id",
            "name",
            "email",
            "password",
            "is_admin",
            "profile_id",
            "profile",
            "tasks",
            "avatar",          # não esqueça da nova coluna
        )

    tasks = fields.List(fields.Nested(TaskSchema))
    name = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.String(required=True)
    is_admin = fields.Boolean(required=True)
    profile_id = fields.Integer(required=False, allow_none=True)
    profile = fields.Nested(ProfileSchema)
