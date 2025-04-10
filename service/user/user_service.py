from app import db
from model.user_model import User
from sqlalchemy.orm import joinedload


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

def create_user(user):
    user_db = User(
        name=user.name, 
        email=user.email, 
        password=user.password, 
        is_admin=user.is_admin,
        profile_id=user.profile_id
    )
    user_db.encrypt_password()
    db.session.add(user_db)
    db.session.commit()
    return user_db

def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return
    db.session.delete(user)
    db.session.commit()

def update_user(previous_user, new_user):
    previous_user.name = new_user.name
    previous_user.email = new_user.email
    previous_user.is_admin = new_user.is_admin

    if new_user.password != previous_user.password:
        previous_user.password = new_user.password
        previous_user.encrypt_password()
    
    if new_user.profile_id:
        previous_user.profile_id = new_user.profile_id

    db.session.commit()

def list_user_id(id):
    return User.query.filter_by(id=id).first()

def list_user_email(email):
    return User.query.filter_by(email=email).first()
