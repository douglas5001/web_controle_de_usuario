from app import db

class Permission(db.Model):
    __tablename__ = "permission"
    __table_args__ = {"schema": "estudos_douglas"}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    route_name = db.Column(db.String(100), nullable=False)
    profile_id = db.Column(db.Integer, db.ForeignKey("estudos_douglas.profile.id"), nullable=False)
    profile = db.relationship("Profile", back_populates="permissions")
