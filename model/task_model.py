from __init__ import db
from user_model import user_task

class Task(db.Model):
    __tablename__ = "task"
    __table_args__ = {"schema": "estudos_douglas"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    event = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    priority = db.Column(db.Integer, nullable=False)
    date_creation = db.Column(db.DateTime)

    users = db.relationship("User", secondary=user_task, back_populates="tasks")