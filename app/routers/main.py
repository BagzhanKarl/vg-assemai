from flask import Blueprint, request, redirect, jsonify

from app.db import Messages, SystemMessages
from app.db.crud import UserApp, create_task
from app.utils import AssemMessage
from app.utils.assemai import AssemAI
from app.utils.search import create_semantic_response
from app.utils.task_system import add_task

main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/webhook/whatsapp', methods=['POST'])
def webhook_whatsapp():
    try:
        post_data = request.get_json()
        if not post_data or 'messages' not in post_data:
            return jsonify({'status': False, 'error': 'Invalid payload'}), 400

        data = post_data['messages'][0]
        phone = data.get('from')
        chat_id = data.get('chat_id')

        if not phone or not chat_id:
            return jsonify({'status': False, 'error': 'Phone or Chat ID missing'}), 400

        # Создаём или обновляем пользователя
        user = UserApp(phone=phone, chat_id=chat_id)
        create_user_result = user.create_user()
        message = AssemMessage()
        # Обрабатываем входящее сообщение
        if 'text' in data:
            message_body = data['text'].get('body')
            if message_body:
                message = Messages(
                    user_id=user.id,
                    role='user',
                    content=message_body,
                    tool_call_id=None,
                    tokens=None
                )
                message.save_to_db()
                add_task(chat_id)
                return jsonify({'status': True, 'data': 'Thanks guys! We take that!'})
        elif 'image' in data:
            ans = ('Спасибо за отправленное изображение! К сожалению, я пока не умею читать содержимое картинок. '
                   'Попробуйте описать текст из изображения словами, и я обязательно помогу вам! 😊')
            response = message.send_text(ans, chat_id)
        elif 'voice' in data:
            ans = ('Спасибо за отправленное голосовое сообщение! Пока я не могу слушать аудиофайлы, но буду рад, '
                   'если вы напишете то же самое текстом. Это поможет мне лучше вам помочь! ')
            response = message.send_text(ans, chat_id)
        else:
            ans = (
                'Я не смог понять отправленное сообщение. Пожалуйста, напишите мне текстом, чтобы мы продолжили общение. '
                'Я здесь, чтобы помочь! ')
            response = message.send_text(ans, chat_id)

        return jsonify({'status': True, 'data': 'Thanks guys! We take that!', 'a': ans})

    except Exception as e:
        return jsonify({'status': False, 'error': str(e)}), 500


@main_bp.route('/check/user', methods=['POST'])
def check_user():
    user = UserApp(user_id=11)
    user.upgrade_user()
    data = user.get_chat()

    message = AssemMessage()
    response = message.send_text("Hello, world!", "77761174378@s.whatsapp.net")
    print(response)


    return data

@main_bp.route('/create/system/', methods=['POST'])
def create_system():
    data = request.form['content']
    prompt = create_semantic_response(query=data)

    # Здесь вы можете добавить код для отправки промпта в GPT mini
    print(prompt)
    return {'ans': prompt}

@main_bp.route('/messages/ai', methods=['POST'])
def chat_with_ai():
    """
    Мы получаем Whapi webhook, сохраняем сообщение и отправителя на базе, вернем ответ на вебхук и создаем задачу для ИИ ассистента
    Каждый 2 минуты проверяем таблицу задач и отвечаем каждому пользователю.
    Уже готова прием вебхука и создание таблицы. А так же готва класс отправка ответа через Whapi

    Осталось сделать функцию который собирает данные, генерирует ответ, и отправляет его на пользователя.
    :return:
    """
    content = request.form['content']
    role = 'user'
    user_id = 12

    ai = Messages(
        user_id=user_id,
        role=role,
        content=content
    )
    ai.save_to_db()
    client = AssemAI(userid=user_id)
    answer = client.generate_answer()

    return {"Status": True, 'answer': answer}