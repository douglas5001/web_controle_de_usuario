from app import ma
from model.user_model import User, Task
from marshmallow import fields

from schema.user.user_schema import UserSchema

class TaskSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        load_instance = True
        fields = ("id", "event", "content", "priority", "date_creation", "users")

    users = fields.List(fields.Nested(UserSchema))
