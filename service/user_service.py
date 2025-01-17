from model.user_model import User
from __init__ import db
def list_user():
    users = User.query.all()
    return users

def create_user(user):
    user_db = User(name=user.name, email=user.email, password=user.password)
    user_db.encrypt_password()
    db.session.add(user_db)
    db.session.commit()
    return user_db

def delete_user(id):
    user = User.query.filter_by(id=id).first()
    db.session.delete(user)
    db.session.commit()
    
def update_user(previous_user, new_user):
    previous_user.name = new_user.name
    previous_user.email = new_user.email
    previous_user.password = new_user.password
    db.session.commit()
    
def list_user_id(id):
    user = User.query.filter_by(id=id).first()
    return user

def list_user_email(email):
    return User.query.filter_by(email=email).first()