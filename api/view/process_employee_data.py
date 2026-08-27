from flask import Blueprint, jsonify, request
from controller.start_employee_pipeline import start_employee_pipeline

process_employee_data_api = Blueprint("process_employee_data", __name__)

@process_employee_data_api.post("/employee/process")
def process_employee_data():
    """
    Starts the employee's data processing pipeline.
    ---
    tags:
        - Employee
    consumes:
        - multipart/form-data
    parameters:
    - name: fileName
      in: formData
      type: string
      required: true
    description:
        Starts (and follows) the pipeline process for employee data. All fields are required.
    responses:
        200:
            status: SUCCESS
    """
    start_employee_pipeline(request.form["fileName"])
    return jsonify({
        "status": "SUCCESS"
    }), 200