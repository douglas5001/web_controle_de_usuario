from app import db
from model.user_model import User

def list_user():
    return User.query.all()

def create_user(user):
    user_db = User(name=user.name, email=user.email, password=user.password, is_admin=user.is_admin)
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
    previous_user.password = new_user.password
    previous_user.is_admin = new_user.is_admin
    if new_user.profile_id:
        previous_user.profile_id = new_user.profile_id
    db.session.commit()

def list_user_id(id):
    return User.query.filter_by(id=id).first()

def list_user_email(email):
    return User.query.filter_by(email=email).first()
