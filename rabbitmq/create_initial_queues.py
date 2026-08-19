import pika

conn = pika.BlockingConnection(pika.ConnectionParameters("localhost", credentials=pika.PlainCredentials("admin", "admin")))
channel = conn.channel()

channel.queue_declare(queue="dead_letter_queue", durable = True)

channel.queue_declare(
    queue = "new_files_queue",
    durable = True,
    arguments = {
        "x-dead-letter-exchange": "", "x-dead-letter-routing-key": "dead_letter_queue"
    }
)

channel.exchange_declare(exchange="file_warning", exchange_type = "fanout")
channel.queue_bind(queue="new_files_queue", exchange = "file_warning")

conn.close()