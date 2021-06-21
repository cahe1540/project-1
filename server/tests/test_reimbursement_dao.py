import time

from daos.reimbursement_dao import ReimbursementDAO
from daos.reimbursement_dao_postgres import ReimbursementDAOPostgres
from entities.reimbursement import Reimbursement
from exceptions.check_violation_error import CheckViolationError
from exceptions.invalid_data_type import InvalidDataTypeException

# unit tests for reimbursement DAOs

# DAO object
from exceptions.reimbursement_not_found_error import ReimbursementNotFoundException
from exceptions.worker_not_found_error import WorkerNotFoundException

reimbursement_dao: ReimbursementDAO = ReimbursementDAOPostgres()


# current epoch time
now = int(time.time())


# TESTS
# CREATE
# success on create reimbursement
def test_create_reimbursement_success():
    sample_reimbursement: Reimbursement = Reimbursement(0, now, 1200.00, "Cocaine for parting", "pending", None, 1, None, None)
    result = reimbursement_dao.create_reimbursement(sample_reimbursement)
    assert result.reimbursement_id != sample_reimbursement.reimbursement_id


# fail on create reimbursement an input is invalid, 400
def test_create_reimbursement_fail():
    try:
        sample_reimbursement: Reimbursement = Reimbursement(0, now, -1111, "", "pending", None, 1, None, None)
        result = reimbursement_dao.create_reimbursement(sample_reimbursement)
        assert False
    except CheckViolationError as e:
        assert (e.code == 400) and (e.summary == "An input argument failed a table constraint")


# fail on create reimbursement the user doesn't exist, 404
def test_create_reimbursement_fail_no_user():
    try:
        sample_reimbursement: Reimbursement = Reimbursement(0, now, 1123, "", "pending", None, 555, None, None)
        result = reimbursement_dao.create_reimbursement(sample_reimbursement)
        assert False
    except WorkerNotFoundException as e:
        assert e.code == 404


# READ
# success on get ALL reimbursement by employee id, return all reimbursements
def test_get_reimbursements_by_employee_id_success():
    results = reimbursement_dao.get_reimbursements_by_employee_id(1)
    assert len(results) > 0


# success on get ALL reimbursements by employee id, but return empty list because none found
def test_get_reimbursements_by_employee_id_success_nothing():
    results = reimbursement_dao.get_reimbursements_by_employee_id(2)
    assert len(results) == 0


# success on get ALL reimbursements by employee id, return empty list, no employee
def test_get_reimbursements_by_employee_id_success_no_employee():
    results = reimbursement_dao.get_reimbursements_by_employee_id(444)
    assert len(results) == 0


# fail on get all reimbursements by employee id, invalid input
def test_get_reimbursements_by_employee_id_fail_bad_value():
    try:
        results = reimbursement_dao.get_reimbursements_by_employee_id("da")
        assert False
    except InvalidDataTypeException as e:
        assert e.code == 500


# success on get ALL reimbursements, return list greater than length 1
def test_get_all_reimbursements_success():
    result = reimbursement_dao.get_all_reimbursements()
    assert len(result) > 0


# UPDATE
# successfully updated a reimbursement
def test_update_reimbursement_by_id():
    reimbursement_list: list[Reimbursement] = reimbursement_dao.get_all_reimbursements()
    result: Reimbursement = reimbursement_dao.update_reimbursement_by_id(reimbursement_list[-1].reimbursement_id, 2, ("approved", "Next time share coke"))
    assert result.manager_id == 2


# fail to update a reimbursement because the reimbursement does not exist, 404
def test_update_reimbursement_by_id_fail_no_record():
    try:
        result: Reimbursement = reimbursement_dao.update_reimbursement_by_id(555, 2, ("approved", "Next time share coke"))
        assert False
    except ReimbursementNotFoundException as e:
        assert e.code == 404


# fail to update reimbursement because manager id does not exist, 404
def test_update_reimbursement_by_id_fail_no_manager():
    try:
        reimbursement_list: list[Reimbursement] = reimbursement_dao.get_all_reimbursements()
        result: Reimbursement = reimbursement_dao.update_reimbursement_by_id(reimbursement_list[-1].reimbursement_id, 555, ("approved", "Next time share coke"))
        assert False
    except WorkerNotFoundException as e:
        assert e.code == 404


# fail to update reimbursement because invalid input for state, 400
def test_update_reimbursement_by_id_fail_invalid_input():
    try:
        result: Reimbursement = reimbursement_dao.update_reimbursement_by_id(1, 2, (5, "Next time share coke"))
        assert False
    except InvalidDataTypeException as e:
        assert e.code == 400


# successfully deleted a reimbursement by id
def test_delete_reimbursement_success():
    reimbursement_list: list[Reimbursement] = reimbursement_dao.get_all_reimbursements()
    deleted = reimbursement_dao.delete_reimbursement(reimbursement_list[-1].reimbursement_id)
    assert deleted.reimbursement_id == reimbursement_list[-1].reimbursement_id


# fail to delete reimbursement, not exist, 404
def test_delete_reimbursement_fail():
    try:
        deleted = reimbursement_dao.delete_reimbursement(5555)
        assert False
    except ReimbursementNotFoundException as e:
        assert e.code == 404