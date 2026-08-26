from minio import Minio
import os
from kafka import KafkaProducer
import json
from models.enums.env_variables import EnvVariables
from models.enums.app_extensions import AppExtensions

def configure_minio(app):

    app.config[EnvVariables.MINIO_ENDPOINT.value] = os.getenv(EnvVariables.MINIO_ENDPOINT.value)
    app.config[EnvVariables.MINIO_ACCESS_KEY.value] = os.getenv(EnvVariables.MINIO_ACCESS_KEY.value)
    app.config[EnvVariables.MINIO_SECRET_KEY.value] = os.getenv(EnvVariables.MINIO_SECRET_KEY.value)
    
    app.extensions[AppExtensions.MINIO.value] = Minio(
        app.config[EnvVariables.MINIO_ENDPOINT.value],
        access_key = app.config[EnvVariables.MINIO_ACCESS_KEY.value],
        secret_key = app.config[EnvVariables.MINIO_SECRET_KEY.value],
        secure = False
    )

def configure_kafka(app):
    app.config[EnvVariables.KAFKA_BOOSTRAP_SERVERS.value] = os.getenv(
        EnvVariables.KAFKA_BOOSTRAP_SERVERS.value
    )

    app.extensions[AppExtensions.KAFKA.value] = KafkaProducer(
        bootstrap_servers= app.config[EnvVariables.KAFKA_BOOSTRAP_SERVERS.value],
        value_serializer=lambda value: json.dumps(value).encode("utf-8")
    )

def configure_swagger():
    return {
        "swagger": "2.0",
        "info": {
        "title":"OSPA API",
        "description": "API responsible for the services regarding the OSPA application. That includes the UI, Minio and Kafka interactions.",
        "version": "1.0.0",
        "contact": {
            "name": "Luiz Otavio",
            "email": "contato.gsluizot@gmail.com",
            }
        }
    }