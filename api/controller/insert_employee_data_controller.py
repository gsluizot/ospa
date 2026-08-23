from flask import current_app
import os
from io import BytesIO
from models.enums.app_extensions import AppExtensions

def insert_csv(file):

    minio_client = current_app.extensions[AppExtensions.MINIO.value]

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
    producer = current_app.extensions[AppExtensions.KAFKA.value]

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