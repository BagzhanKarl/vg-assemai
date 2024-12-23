import json
from datetime import datetime
from openai import OpenAI

from app.db import SystemMessages, Messages, User, db


class AssemAI:
    def __init__(self, userid):
        self.model = 'gpt-4o-mini'
        self.key = ''
        self.realtime = datetime.now()
        self.chat_id = userid

    def save_user_on_memory(self, fullname, chatid, branch):
        user = User.query.get(self.chat_id)
        user.name = fullname
        user.branch = branch
        db.session.add(user)
        db.session.commit()
        return True

    def create_context_for_ai(self):
        system_messages = SystemMessages.query.all()
        user = User.query.filter_by(id=self.chat_id).first()

        fullname = user.name if user.name else "неизвестно (необходимо ОБЕЗАТЕЛЬНО узнать)"
        branch = user.branch if user.branch else "неизвестно (необходимо ОБЕЗАТЕЛЬНО узнать)"
        userdata = f'Полное имя: {fullname}, филиал: {branch}, номер телефона: {user.phone}, chat_id: {user.chat_id}'

        data = [
            {
                'role': 'developer',
                'content': 'Вы бот от команды Assem, который создан использвуя gpt-4o с api ключами OpenAI. Ваша задача помочь пользователям в обучений Бережливого Производство. Если нету информаций о человеке, посторайтесь узнать инфу, полное имя и с какой он компании и филиала. Потом сохраняейте эту информацию!'
            },
            {
                'role': 'developer',
                'content': f'Информация о пользователя: {userdata}. Без этих данных ЗАПРЕШЕНО отвечать на вопросы на пользователя, узнайте сначало!, Реальное время на данный момент: {self.realtime}'
            }
        ]
        for message in system_messages:
            data.append({
                'role': 'developer',
                'content': message.content,
            })
        user_chat = Messages.get_messages_by_user(user_id=self.chat_id)
        for text in user_chat:
            if 'role' in text and 'content' in text:
                if text.get('tool_call'):
                    if text.get('content') != None:
                        data.append({
                            'role': 'tool',
                            'content': 'вызывано функция',
                            'tool_call': text['tool_call'],
                            'toll_call_id': text.get('toll_call_id'),  # Используем get, чтобы избежать ошибок
                        })
                else:
                    data.append({
                        'role': text['role'],
                        'content': text['content'],
                    })
            else:
                raise ValueError(f"Неверная структура контекста: {text}")
        return data

    def generate_answer(self, attempt=0, max_attempts=2):
        context = self.create_context_for_ai()
        client = OpenAI(api_key=self.key)
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "save_user_on_memory",
                    "description": "The function saves the name and branch the person works in, as well as the chat ID in the database, so that you remember the user next time.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "full_name": {"type": "string"},
                            "branch": {"type": "string"},
                            "chat_id": {"type": "string"},
                        },
                        "required": ["full_name", "branch", "chat_id"],
                        "additionalProperties": False
                    },
                },
            }
        ]
        completion = client.chat.completions.create(
            model=self.model,
            messages=context,
            tools=tools,
        )
        if hasattr(completion.choices[0].message, 'content') and completion.choices[0].message.content:
            answer = Messages(
                user_id=self.chat_id,
                role=completion.choices[0].message.role,
                content=completion.choices[0].message.content

            )
            answer.save_to_db()

        if hasattr(completion.choices[0].message, 'tool_calls') and completion.choices[0].message.tool_calls:
            tool_call = completion.choices[0].message.tool_calls[0]
            if tool_call.function.name == 'save_user_on_memory':
                arguments = json.loads(tool_call.function.arguments)
                full_name = arguments.get('full_name')
                branch = arguments.get('branch')
                chat_id = arguments.get('chat_id')
                self.save_user_on_memory(fullname=full_name, chatid=chat_id, branch=branch)
                answer = Messages(
                    user_id=self.chat_id,
                    role='system',
                    content='Успешно сохранено информация о пользователе'
                )
                answer.save_to_db()
                return self.generate_answer(attempt=attempt+1, max_attempts=max_attempts)
        else:
            return completion.choices[0].message.content
        return completion.choices[0].message.content
