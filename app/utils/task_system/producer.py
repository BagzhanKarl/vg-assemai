from pika import ConnectionParameters, BlockingConnection
import redis

connectoion_params = ConnectionParameters(
    host="localhost",
    port=5672,
)

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

def add_task(chat_id):
    # Проверяем, есть ли уже chat_id
    if redis_client.exists(chat_id):
        print(f"Task with chat_id {chat_id} already exists. Skipping...")
        return

    # Добавляем chat_id в Redis
    redis_client.set(chat_id, "exists")

    # Публикуем в RabbitMQ
    with BlockingConnection(connectoion_params) as conn:
        with conn.channel() as ch:
            ch.queue_declare(queue="ai-tasks")
            ch.basic_publish(
                exchange="",
                routing_key="ai-tasks",
                body=chat_id,
            )
    print(f"Task with chat_id {chat_id} added successfully.")
