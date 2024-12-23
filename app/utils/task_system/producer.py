from pika import ConnectionParameters, BlockingConnection

connectoion_params = ConnectionParameters(
    host="localhost",
    port=5672,
)

def add_task(chat_id):


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
