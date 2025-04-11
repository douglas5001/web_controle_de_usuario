from app import db
from model.permission_model import Permission
from model.profile_model import Profile
from sqlalchemy.orm import joinedload

from model.user_model import User

def create_profile(nome):
    perfil = Profile(name=nome)
    db.session.add(perfil)
    db.session.commit()
    return perfil

def list_profiles():
    return Profile.query.all()

def get_profile_by_id(profile_id):
    return Profile.query.filter_by(id=profile_id).first()

def list_profile_page(page, per_page, search=None, search_field="name"):
    query = Profile.query
    if search:
        padrao_busca = f"%{search}%"
        if search_field == "name":
            query = query.filter(Profile.name.ilike(padrao_busca))
    return query.order_by(Profile.id).paginate(page=page, per_page=per_page, error_out=False)


def update_profile_with_permissions(perfil_existente, novo_nome, novas_permissoes):
    perfil_existente.name = novo_nome

    # Remove todas as permissões antigas
    for perm in perfil_existente.permissions:
        db.session.delete(perm)
    db.session.commit()

    # Cria novas permissões
    for p in novas_permissoes:
        nova = Permission(route_name=p, profile_id=perfil_existente.id)
        db.session.add(nova)

    db.session.commit()
    return perfil_existente

def delete_profile(profile_id):
    perfil = Profile.query.filter_by(id=profile_id).first()
    if not perfil:
        return None

    # Remove o vínculo dos usuários com esse perfil
    User.query.filter_by(profile_id=profile_id).update({User.profile_id: None})

    # Agora pode excluir o perfil com segurança
    db.session.delete(perfil)
    db.session.commit()
    return perfil
