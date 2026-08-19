from flask import Blueprint, jsonify, request
from controller.insert_employee_data_controller import insert_csv, register_event

insert_employee_data_api = Blueprint("insert_employee_data", __name__)

@insert_employee_data_api.post("/employee/insert")
def insert_employee_data():
    """
    Insert employees inside the minio bucket.
    ---
    consumes:
        - multipart/form-data
    parameters:
    - name: csv
      in: formData
      type: file
      required: true
    description: 
        Insert data inside the minio bucket. For it to work properly, you must provide a csv file with the exact same column names as below\n\n
        Employee_ID – Unique identifier for each employee\n
        Employee_Name – Randomly generated full name\n
        Age – Employee's age (22 to 60 years)\n
        Country – Country of employment (chosen from 10 countries)\n
        Department – Assigned department (HR, Finance, Engineering, etc.)\n
        Position – Employee's job role (Manager, Developer, Analyst, etc.)\n
        Salary – Annual salary (randomly generated between $30,000 and $150,000)\n
        Joining_Date – Employee's start date (randomly selected from the past 10 years)\n
    responses:
        200: 
            description: Success
    """
    if "csv" not in request.files:
        return jsonify({
            "status":"error",
            "message": "CSV File is required"
        })

    csv_file = request.files["csv"]

    if csv_file.filename == "":
        return jsonify({
            "status": "error",
            "message": "No file selected"
        }), 400
 
    if not csv_file.filename.lower().endswith(".csv"):
        return jsonify({
            "status": "error",
            "message": "File must be a CSV"
        }), 400
 
    try:
        result = insert_csv(csv_file)
        register_event("ospa", "bronze/employee_records.csv")
        return jsonify(result), 200
 
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
        }), 500