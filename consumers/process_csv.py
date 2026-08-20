import pika, json
import pandas as pd
from minio import Minio
from io import BytesIO

def process_csv(channel, method, properties, body):
    try:
        event = json.loads(body)
        # TODO: Verify nulls and notify them later
        # TODO: Verify if there are duplicates on employee_id and notify
        # TODO: Verify if age is less than 14 and higher than 100
        # TODO: Verify data types

        minio_client = Minio(
        "localhost:9000",
        access_key = "minioadmin",
        secret_key = "minioadmin",
        secure = False
        )

        BUCKET = event["bucket"]
        FILE_PATH = event["key"]

        response = minio_client.get_object(BUCKET, FILE_PATH)
        data = response.read()
        response.close()
        response.release_conn()

        df = pd.read_csv(BytesIO(data))

        print(df.isnull().sum())
        # TODO: Returns the amount of nulls if any to the final user

        channel.basic_ack(delivery_tag = method.delivery_tag)
    except Exception as e:
        print(f"Error: {e}")
        channel.basic_nack(delivery_tag = method.delivery_tag, requeue = False)

conn = pika.BlockingConnection(pika.ConnectionParameters("localhost", credentials=pika.PlainCredentials("admin", "admin")))
channel = conn.channel()
channel.basic_consume(queue = "new_files_queue", on_message_callback=process_csv)

print("Waiting for files...")
channel.start_consuming()