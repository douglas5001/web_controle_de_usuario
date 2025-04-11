from app import db
from model.permission_model import Permission

def grant_permission_to_profile(profile_id: int, route_name: str) -> Permission:
    permissao_existente = Permission.query.filter_by(profile_id=profile_id, route_name=route_name).first()
    
    if permissao_existente:
        return permissao_existente
    
    nova_permissao = Permission(profile_id=profile_id, route_name=route_name)
    db.session.add(nova_permissao)
    db.session.commit()
    return nova_permissao

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
    return any(permission.route_name == route_name for permission in user.profile.permissions)
