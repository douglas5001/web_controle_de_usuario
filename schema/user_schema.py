from app import ma
from model.user_model import User, Task
from marshmallow import fields

class TaskSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        load_instance = True
        fields = ("id", "event", "content", "priority", "date_creation")

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        fields = ("id", "name", "email", "password", "is_admin", "tasks")

    tasks = fields.List(fields.Nested(TaskSchema))
    name = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.String(required=True)
    is_admin = fields.Boolean(required=True)