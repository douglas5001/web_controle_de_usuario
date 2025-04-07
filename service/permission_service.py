from app import db
from model.permission_model import Permission

def grant_permission_to_profile(profile_id, route_name):
    permission = Permission(route_name=route_name, profile_id=profile_id)
    db.session.add(permission)
    db.session.commit()

def revoke_permission_from_profile(profile_id, route_name):
    permission = Permission.query.filter_by(profile_id=profile_id, route_name=route_name).first()
    if permission:
        db.session.delete(permission)
        db.session.commit()

def user_has_permission(user, route_name):
    if user.is_admin:
        return True
    if not user.profile:
        return False
    return bool(
        user.profile.permissions.filter_by(route_name=route_name).first()
    )
