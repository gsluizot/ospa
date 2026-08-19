from minio import Minio
import os
from io import BytesIO
import pika, json

def insert_csv(file):

    minio_client = Minio(
        "localhost:9000",
        access_key = "minioadmin",
        secret_key = "minioadmin",
        secure = False
    )

    BUCKET = "ospa"

    filename = os.path.basename(file.filename)
    object_name = f"bronze/{filename}"

    file_data = file.read()

    minio_client.put_object(
        bucket_name = BUCKET,
        object_name = object_name,
        data = BytesIO(file_data),
        length = len(file_data),
        content_type = "text/csv",
    )

    return "SUCCESS"

def register_event(bucket, key_file):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost", credentials=pika.PlainCredentials("admin", "admin"))
    )
    channel = connection.channel()

    warning = {
        "bucket": bucket,
        "key": key_file,
    }

    channel.basic_publish(
        exchange="file_warning",
        routing_key = "",
        body = json.dumps(warning),
        properties = pika.BasicProperties(delivery_mode= 2)
    )
    connection.close()