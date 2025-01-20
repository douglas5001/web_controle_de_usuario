from __init__ import db
from passlib.hash import pbkdf2_sha256

# Tabela de associação para relação n para n
user_task = db.Table(
    'user_task',
    db.Column('user_id', db.Integer, db.ForeignKey('estudos_douglas.user.id'), primary_key=True),
    db.Column('task_id', db.Integer, db.ForeignKey('estudos_douglas.task.id'), primary_key=True),
    schema="estudos_douglas"
)

class User(db.Model):
    __tablename__ = "user"
    __table_args__ = {"schema": "estudos_douglas"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean)

    tasks = db.relationship("Task", secondary=user_task, back_populates="users")

    def encrypt_password(self):
        self.password = pbkdf2_sha256.hash(self.password)

    def show_password(self, password):
        return pbkdf2_sha256.verify(password, self.password)


class Task(db.Model):
    __tablename__ = "task"
    __table_args__ = {"schema": "estudos_douglas"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    event = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    priority = db.Column(db.Integer, nullable=False)
    date_creation = db.Column(db.DateTime)

    users = db.relationship("User", secondary=user_task, back_populates="tasks")
