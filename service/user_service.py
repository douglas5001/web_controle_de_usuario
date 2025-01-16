from model.user_model import User
from __init__ import db
def list_user():
    users = User.query.all()
    return users

def create_user(user):
    user_db = User(name=user.name, email=user.email, password=user.password)
    
    db.session.add(user_db)
    db.session.commit()
    return user_db

def delete_user(id):
    user = User.query.filter_by(id=id).first()
    db.session.delete(user)
    db.session.commit()