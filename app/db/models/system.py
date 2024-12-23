from datetime import datetime
from app.db import db



def delete_data(id):
    delete = SystemMessages.query.get(id)
    db.session.delete(delete)
    db.session.commit()

class SystemMessages(db.Model):
    __tablename__ = 'system_messages'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __init__(self, content, id=None):
        self.content = content
        self.id = id

    def create_system_saver(self):
        """
        Сохраняет сообщение в базу данных.
        """
        try:
            db.session.add(self)  # Добавляем текущий экземпляр
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def edit_system_saver(self):
        edit = SystemMessages.query.get(self.id)
        edit.content = self.content
        edit.updated_at = datetime.now()
        db.session.commit()
        return True

