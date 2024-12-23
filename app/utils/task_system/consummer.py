from pika import ConnectionParameters, BlockingConnection

connectoion_params = ConnectionParameters(
    host="localhost",
    port=5672,
)

def process_task(ch, method, properties, body):
    print(" [x] Received %r" % body)

    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    with BlockingConnection(connectoion_params) as conn:
        with conn.channel() as ch:
            ch.queue_declare(queue="ai-tasks")

            ch.basic_consume(
                queue="ai-tasks",
                on_message_callback=process_task,
            )

            ch.start_consuming()

if __name__ == "__main__":
    main()
