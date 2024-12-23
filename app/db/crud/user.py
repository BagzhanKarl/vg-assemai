from app.db import User, db, Messages
import logging

logging.basicConfig(level=logging.ERROR)

class UserApp:
    def __init__(self, phone=None, chat_id=None, name=None, branch=None, user_id=None):
        self.id = user_id
        self.phone = phone
        self.chat_id = chat_id
        self.name = name
        self.branch = branch

    def upgrade_user(self):
        if self.id is None:
            return {'status': False, 'data': 'Нету ID пользователя'}

        user = User.query.get(self.id)
        self.phone = user.phone
        self.chat_id = user.chat_id
        self.name = user.name
        self.branch = user.branch
        return {'status': True, 'data': {'id': self.id, 'phone': self.phone, 'chat_id': self.chat_id}}

    def create_user(self):
        try:
            # Проверяем, существует ли пользователь с таким chat_id
            existing_user = User.query.filter_by(chat_id=self.chat_id).first()
            if existing_user:
                # Устанавливаем данные существующего пользователя в объект
                self.id = existing_user.id
                self.phone = existing_user.phone
                self.name = existing_user.name
                self.branch = existing_user.branch
                return {"success": False, "error": "User already exists.", "user_id": self.id}

            # Создаем нового пользователя
            user = User(
                phone=self.phone,
                chat_id=self.chat_id,
                name=self.name,
                branch=self.branch
            )
            db.session.add(user)
            db.session.flush()  # Сохраняем и получаем ID
            self.id = user.id  # Устанавливаем ID в текущем объекте
            db.session.commit()
            return {"success": True, "user_id": user.id}
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error creating user: {e}")
            return {"success": False, "error": str(e)}

    def get_user(self):
        if not self.id:
            return {"success": False, "error": "User ID is required."}
        user = User.query.get(self.id)
        if user is None:
            return {"success": False, "error": "User not found."}
        return {"success": True, "user_id": user.id}

    def update_user(self):
        if not self.id:
            return {"success": False, "error": "User ID is required."}
        user = User.query.get(self.id)
        if user is None:
            return {"success": False, "error": "User not found."}
        user.name = self.name
        user.branch = self.branch
        try:
            db.session.commit()
            return {"success": True, "user_id": user.id}
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error updating user: {e}")
            return {"success": False, "error": str(e)}

    def save_message(self, role, content, tokens=None):
        if not self.id:
            return {"success": False, "error": "User ID is required."}

        message = Messages(
            role=role,
            content=content,
            name=role,  # Возможно, тут ошибка.
            user_id=self.id,
            tokens=tokens
        )
        try:
            db.session.add(message)
            db.session.commit()
            return {"success": True, "message_id": message.id}
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error saving message: {e}")
            return {"success": False, "error": str(e)}

    def get_chat(self):
        if not self.id:
            return {"success": False, "error": "User ID is required."}

        try:
            messages = Messages.query.filter_by(user_id=self.id).all()
            context = [
                {
                    "role": message.role,
                    "content": message.content,
                    "name": message.name,
                }
                for message in messages
            ]
            return {"success": True, "context": context}
        except Exception as e:
            logging.error(f"Error retrieving chat: {e}")
            return {"success": False, "error": str(e)}