from app.db import db, Default

class User(Default):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(20), nullable=False)
    chat_id = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=True)
    branch = db.Column(db.String(100), nullable=True)