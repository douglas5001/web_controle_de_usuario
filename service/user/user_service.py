from app import db
from model.user_model import User
from sqlalchemy.orm import joinedload

from service.user.file_service import delete_avatar, save_avatar


def list_user(page, per_page, search=None, search_field="name"):
    query = User.query.options(joinedload(User.profile))
    if search:
        search_pattern = f"%{search}%"
        if search_field == "name":
            query = query.filter(User.name.ilike(search_pattern))
        elif search_field == "email":
            query = query.filter(User.email.ilike(search_pattern))
        elif search_field == "profile":
            from model.profile_model import Profile
            query = query.join(Profile).filter(Profile.name.ilike(search_pattern))
    return query.order_by(User.id).paginate(page=page, per_page=per_page, error_out=False)

def create_user(user, file_storage):
    if file_storage:
        try:
            avatar_filename = save_avatar(file_storage)
            user.avatar = avatar_filename
        except ValueError as e:
            raise ValueError(str(e))

    # 🔐 Criptografa a senha antes de salvar
    user.encrypt_password()

    db.session.add(user)
    db.session.commit()

def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return
    db.session.delete(user)
    db.session.commit()

def update_user(
    previous_user,
    new_user,
    file_storage=None,
    remove_avatar=False,
    change_password=False,
    ):
    previous_user.name     = new_user.name
    previous_user.email    = new_user.email
    previous_user.is_admin = new_user.is_admin

    if change_password:
        previous_user.password = new_user.password
        previous_user.encrypt_password()

    # --- PERFIL -------------------------------------------------------------
    # Atualiza ou remove perfil conforme escolha do usuário
    previous_user.profile_id = new_user.profile_id   # ← linha única resolve

    # ------------------------------------------------------------------------
    if remove_avatar:
        delete_avatar(previous_user.avatar)
        previous_user.avatar = None

    if file_storage and file_storage.filename:
        delete_avatar(previous_user.avatar)
        previous_user.avatar = save_avatar(file_storage)

    db.session.commit()

def list_user_id(id):
    return User.query.filter_by(id=id).first()

def list_user_email(email):
    return User.query.filter_by(email=email).first()
