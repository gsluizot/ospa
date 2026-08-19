import pika, json

def process_csv(channel, method, properties, body):
    try:
        warning = json.loads(body)
        key_file = warning["key"]
        print(f"New File: {key_file}")

        channel.basic_ack(delivery_tag = method.delivery_tag)
    except Exception as e:
        print(f"Error: {e}")
        channel.basic_nack(delivery_tag = method.delivery_tag, requeue = False)

conn = pika.BlockingConnection(pika.ConnectionParameters("localhost", credentials=pika.PlainCredentials("admin", "admin")))
channel = conn.channel()
channel.basic_consume(queue = "new_files_queue", on_message_callback=process_csv)

print("Waiting for files...")
channel.start_consuming()