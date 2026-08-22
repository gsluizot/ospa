import pika, json
import pandas as pd
from minio import Minio
from io import BytesIO
from kafka import KafkaConsumer

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

comsumer = KafkaConsumer(
    "file-warning",
    bootstrap_servers= "localhost:9092",
    value_deserializer=lambda value: json.loads(value.decode("utf-8")),
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id= "csv_processor_group"
)

print("Waiting for files...")
for message in comsumer:
    event = message.value
    process_csv(event)