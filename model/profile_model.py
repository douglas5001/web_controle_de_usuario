from app import db
from model.permission_model import Permission

class Profile(db.Model):
    __tablename__ = "profile"
    __table_args__ = {"schema": "estudos_douglas"}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    permissions = db.relationship(
        "Permission",
        back_populates="profile",
        cascade="all, delete-orphan"
    )
