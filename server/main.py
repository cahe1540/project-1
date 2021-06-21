from flask import Flask, request
from flask_cors import CORS

from services.app_services_impl import AppServicesImpl
from daos.reimbursement_dao_postgres import ReimbursementDAOPostgres
from daos.worker_dao_postgres import WorkerDAOPostgres
from entities.worker import Worker
from entities.reimbursement import Reimbursement
from utils.remove_passwords import remove_passwords
from utils.json_response import json_response
from utils.handle_exceptions import handle_exceptions
import logging

logging.basicConfig(filename="records.log", level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(message)s')

services: AppServicesImpl = AppServicesImpl(WorkerDAOPostgres(),ReimbursementDAOPostgres())

app = Flask(__name__)
CORS(app)


# login send info in query params
@app.route("/users/login", methods=["GET"])
@handle_exceptions
def login():
    user_name = password = ""
    if request.args:
        user_name = request.args["user_name"]
        password = request.args["password"]

    worker: Worker = services.retrieve_worker_by_user_name_and_password(user_name, password)
    worker_json_no_password = remove_passwords(worker.as_json_dict())
    return json_response("Success", 200, worker_json_no_password), 200


# get all employees
@app.route("/employees", methods=["GET"])
@handle_exceptions
def get_all_employees():
    workers = services.retrieve_all_employees()
    json_list = [el.as_json_dict() for el in workers]
    return json_response("success", 200, json_list), 200


# get all reimbursements by employee id
@app.route("/employees/<employee_id>/reimbursements", methods=["GET"])
@handle_exceptions
def get_reimbursements_by_employee(employee_id: str):
    reimbursements = services.retrieve_reimbursements_by_employee_id(int(employee_id))
    json_list = [el.as_json_dict() for el in reimbursements]
    return json_response("success", 200, json_list), 200


# employee create reimbursement send data in json
@app.route("/reimbursements", methods=["POST"])
@handle_exceptions
def create_reimbursement():
    body = request.json.values()
    new_reimbursement = services.add_reimbursement(Reimbursement(*body))
    return json_response("success", 201, new_reimbursement.as_json_dict()), 201


# manager gets all reimbursements
@app.route("/reimbursements", methods=["GET"])
@handle_exceptions
def get_all_reimbursements():
    reimbursements = services.retrieve_all_reimbursements()
    json_list = [reimbursement.as_json_dict() for reimbursement in reimbursements]
    return json_response("success", 200, json_list), 200


# manager updates reimbursements
@app.route("/managers/<manager_id>/reimbursements/<reimbursement_id>", methods=["PATCH"])
@handle_exceptions
def manager_accept_reject_reimbursement(manager_id: str, reimbursement_id: str):
    body = request.json.values()
    updated = services.update_reimbursement_by_id(int(reimbursement_id), int(manager_id), (*body,))
    return json_response("success", 200, updated.as_json_dict()), 200


# employee deletes own reimbursement only if pending
@app.route("/employees/<employee_id>/reimbursements/<reimbursement_id>", methods=["DELETE"])
@handle_exceptions
def employee_deletes_reimbursement(reimbursement_id: str, employee_id: str):
    deleted = services.delete_own_reimbursement_by_id(int(reimbursement_id), int(employee_id))
    return json_response("success", 204, deleted.as_json_dict()), 204


if __name__ == '__main__':
    app.run(debug=True, port=1313)


