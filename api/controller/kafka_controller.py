from flask import current_app
from models.enums.app_extensions import AppExtensions

def register_event(event):
    producer = current_app.extensions[AppExtensions.KAFKA.value]

    producer.send(
        "file_processing",
        value=event,
    )
    producer.flush()
    producer.close()