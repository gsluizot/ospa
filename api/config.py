from minio import Minio
from dotenv import load_dotenv
import os

def configure_minio(app):
    load_dotenv()

    app.config["MINIO_ENDPOINT"] = os.getenv("MINIO_ENDPOINT")
    app.config["MINIO_ACCESS_KEY"] = os.getenv("MINIO_ACCESS_KEY")
    app.config["MINIO_SECRET_KEY"] = os.getenv("MINIO_SECRET_KEY")
    
    app.extensions["minio"] = Minio(
        app.config["MINIO_ENDPOINT"],
        access_key = app.config["MINIO_ACCESS_KEY"],
        secret_key = app.config["MINIO_SECRET_KEY"],
        secure = False
    )
    