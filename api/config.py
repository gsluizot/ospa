from minio import Minio
import os
from kafka import KafkaProducer
import json

def configure_minio(app):

    app.config["MINIO_ENDPOINT"] = os.getenv("MINIO_ENDPOINT")
    app.config["MINIO_ACCESS_KEY"] = os.getenv("MINIO_ACCESS_KEY")
    app.config["MINIO_SECRET_KEY"] = os.getenv("MINIO_SECRET_KEY")
    
    app.extensions["minio"] = Minio(
        app.config["MINIO_ENDPOINT"],
        access_key = app.config["MINIO_ACCESS_KEY"],
        secret_key = app.config["MINIO_SECRET_KEY"],
        secure = False
    )

def configure_kafka(app):
    app.config["KAFKA_BOOSTRAP_SERVERS"] = os.getenv(
        "KAFKA_BOOSTRAP_SERVERS"
    )

    app.extensions["kafka_producer"] = KafkaProducer(
        bootstrap_servers= app.config["KAFKA_BOOSTRAP_SERVERS"],
        value_serializer=lambda value: json.dumps(value).encode("utf-8")
    )