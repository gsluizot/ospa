from minio import Minio
import os
from io import BytesIO
import json
from kafka import KafkaProducer

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
    producer = KafkaProducer(
        bootstrap_servers = 'localhost:9092',
        value_serializer = lambda value: json.dumps(value).encode("utf-8")
    )

    warning = {
        "bucket": bucket,
        "key": key_file,
    }

    producer.send(
        "file_warning",
        value=warning,
    )
    producer.flush()
    producer.close()