from __init__ import db

class User(db.Model):
    __tablename__ = "user"
    __table_args__ = {"schema": "schema_estudo"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
