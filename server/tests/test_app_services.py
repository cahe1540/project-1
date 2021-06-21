from unittest.mock import Mock, MagicMock

from entities.worker import Worker
from entities.reimbursement import Reimbursement
from services.app_services_impl import AppServicesImpl
from daos.reimbursement_dao_postgres import ReimbursementDAOPostgres
from daos.worker_dao_postgres import WorkerDAOPostgres
from exceptions.worker_not_found_error import WorkerNotFoundException
from exceptions.unauthorized_action_error import UnauthorizedActionException


worker_dao = WorkerDAOPostgres()
reimbursement_dao = ReimbursementDAOPostgres()
services = AppServicesImpl(worker_dao, reimbursement_dao)


# only need to test retrieve reimbursement by employee ID


# pass get reimbursements by employee ID
def test_retrieve_reimbursement_by_employee_id():
    mock = MagicMock(return_value= [1,2,3,4])
    services.reimbursementDao.retrieve_reimbursements_by_employee_id = mock
    reimbursements = services.retrieve_reimbursements_by_employee_id(1)
    assert len(reimbursements) >= 0


# fail because employee ID not exist, 404
def test_retrieve_reimbursement_by_employee_id_fail():
    mock = MagicMock(side_effect = WorkerNotFoundException("", "", 404))
    services.reimbursementDao.retrieve_reimbursements_by_employee_id = mock
    try:
        reimbursements = services.retrieve_reimbursements_by_employee_id(55555)
        assert False
    except WorkerNotFoundException as e:
        assert e.code == 404


# delete reimbursement by both ids success
def test_delete_reimbursement():
    mock1 = MagicMock(return_value = Worker(1,"x","t","y",None,"avc","df"))
    services.workerDao.get_worker_by_id = mock1
    mock2 = MagicMock(return_value = [Reimbursement(99,0,0,"a","b",None,1,None, None)])
    services.reimbursementDao.get_reimbursements_by_employee_id = mock2
    mock3 = MagicMock(return_value = Reimbursement(99,0,0,"a","b",None,1,None, None))
    services.reimbursementDao.delete_reimbursement = mock3
    reimbursement = services.delete_own_reimbursement_by_id(99,1)
    assert reimbursement.reimbursement_id == 99


# delete reimbursement fail because worke not exist 404
def test_delete_reimbursement_fail_no_worker():
    mock1 = Mock(side_effect = WorkerNotFoundException("", "", 404))
    services.workerDao.get_worker_by_id = mock1
    try:
        reimbursement = services.delete_own_reimbursement_by_id(1,5)
        assert False
    except WorkerNotFoundException as e:
        assert e.code == 404


# fail to delete reimbursement because it belongs to someone else
def test_delete_reimbursement_fail_no_reimbursement_exists():
    mock1 = MagicMock(return_value = Worker(1,"x","t","y",None,"avc","df"))
    services.workerDao.get_worker_by_id = mock1
    mock2 = Mock(side_effect = UnauthorizedActionException("", "", 401))
    services.reimbursementDao.delete_reimbursement = mock2
    try:
        reimbursement = services.delete_own_reimbursement_by_id(99,1)
        assert reimbursement.reimbursement_id == 99
    except UnauthorizedActionException as e:
        assert e.code == 401
