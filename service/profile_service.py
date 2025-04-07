from app import db
from model.profile_model import Profile

def create_profile(name):
    profile = Profile(name=name)
    db.session.add(profile)
    db.session.commit()
    return profile

def list_profiles():
    return Profile.query.all()

def get_profile_by_id(profile_id):
    return Profile.query.filter_by(id=profile_id).first()
