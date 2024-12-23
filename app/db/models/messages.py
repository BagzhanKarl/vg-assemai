from app.db import db

class Messages(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    role = db.Column(db.String(15), nullable=False)  # user, assistant, tool, etc.
    content = db.Column(db.Text, nullable=True)  # JSON для хранения вложенных структур (например, type, text)
    tool_call = db.Column(db.Text, nullable=True)
    tool_call_id = db.Column(db.String(50), nullable=True)  # ID вызова инструмента (если применимо)
    tokens = db.Column(db.String(100), nullable=True)  # Хранение токенов или метаданных

    def __init__(self, user_id, role, content, tool_call_id=None, tool_call=None, tokens=None):
        self.user_id = user_id
        self.role = role
        self.content = content
        self.tool_call = tool_call
        self.tool_call_id = tool_call_id
        self.tokens = tokens

    def save_to_db(self):
        """
        Сохраняет сообщение в базу данных.
        """
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    @classmethod
    def get_messages_by_user(cls, user_id):
        """
        Получает все сообщения пользователя по его ID.
        """
        context = []
        messages = Messages.query.filter_by(user_id=user_id).all()
        for message in messages:
            if message.tool_call:
                context.append({
                    "role": message.role,
                    "content": message.content,
                    "tool_call": message.tool_call,
                    "tool_call_id": message.tool_call_id,
                })
            else:
                context.append({
                    "role": message.role,
                    "content": message.content,
                })
        return context

    @classmethod
    def get_message_by_tool_call_id(cls, tool_call_id):
        """
        Получает сообщение по идентификатору вызова инструмента.
        """
        return cls.query.filter_by(tool_call_id=tool_call_id).first()
