from app import ma
from model.profile_model import Profile
from marshmallow import fields

class ProfileSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Profile
        load_instance = True
        fields = ("id", "name")
