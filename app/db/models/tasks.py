from app.db import db, Default

class Task(Default):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    status = db.Column(db.String(25)) #pending, completed
    tasktype = db.Column(db.String(100)) #sendtext, generate, sendfile

