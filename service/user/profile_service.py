from app import db
from model.profile_model import Profile
from sqlalchemy.orm import joinedload

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

def update_profile(perfil_existente, novo_nome):
    perfil_existente.name = novo_nome
    db.session.commit()
    return perfil_existente

def delete_profile(profile_id):
    perfil = Profile.query.filter_by(id=profile_id).first()
    if perfil:
        db.session.delete(perfil)
        db.session.commit()
    return perfil
