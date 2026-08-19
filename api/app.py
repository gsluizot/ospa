from flask import Flask
from flasgger import Swagger

from view.insert_employee_data import insert_employee_data_api

def create_app():
    app = Flask(__name__)
    Swagger(app)

    app.register_blueprint(insert_employee_data_api)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug = True)
