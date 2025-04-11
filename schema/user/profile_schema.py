from app import ma
from model.profile_model import Profile
from marshmallow import fields

from schema.user.permission_schema import PermissionSchema

class ProfileSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Profile
        load_instance = True
        fields = ("id", "name", "permissions")

    permissions = fields.List(fields.Nested(PermissionSchema))