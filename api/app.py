from flask import Flask
from flasgger import Swagger
from config import configure_minio, configure_kafka, configure_swagger
from dotenv import load_dotenv

from view.insert_employee_data import insert_employee_data_api
from view.process_employee_data import process_employee_data_api

def create_app():
        
    app = Flask(__name__)
    load_dotenv()

    configure_minio(app)
    configure_kafka(app)

    Swagger(app, template=configure_swagger())

    app.register_blueprint(insert_employee_data_api)
    app.register_blueprint(process_employee_data_api)

    return app

app = create_app()

if __name__ == "__main__":
    port = input("Please select the port: ")
    app.run(debug = True, port=port)
