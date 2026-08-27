from flask import current_app
from models.enums.app_extensions import AppExtensions

def register_event(event: dict):
    """
    Register an event at kafka stream. Event must be a dictionary. The event will be registered exactly as the dictionary used.

    Example:
    {
        "status": "PROCESSING_NULLS_OK"
    }
    """
    producer = current_app.extensions[AppExtensions.KAFKA.value]

    producer.send(
        "file_processing",
        value=event,
    )
    producer.flush()
    producer.close()