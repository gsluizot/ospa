from flask import current_app
from models.enums.app_extensions import AppExtensions
import pandas as pd
from io import BytesIO

def start_employee_pipeline(file_path: str):
    try:
        # TODO: Verify nulls and notify them later
        # TODO: Verify if there are duplicates on employee_id and notify
        # TODO: Verify if age is less than 14 and higher than 100
        # TODO: Verify data types
        BUCKET = "ospa"
        minio_client = current_app.extensions[AppExtensions.MINIO.value]

        response = minio_client.get_object(BUCKET, file_path)
        data = response.read()
        response.close()
        response.release_conn()

        df = pd.read_csv(BytesIO(data))

        print(df.isnull().sum())
        return "SUCCESS"
    except Exception as e:
        print(f"Error: {e}")

