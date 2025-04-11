# schema/user/permission_schema.py
from app import ma
from model.permission_model import Permission

class PermissionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Permission
        load_instance = True
        fields = ("route_name",)