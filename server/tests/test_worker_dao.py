from daos.worker_dao import WorkerDAO
from daos.worker_dao_postgres import WorkerDAOPostgres
from exceptions.invalid_login_error import InvalidLoginException
from exceptions.worker_not_found_error import WorkerNotFoundException
from exceptions.invalid_data_type import InvalidDataTypeException

worker_dao: WorkerDAO = WorkerDAOPostgres()


# successfully retrived all workers
def test_get_all_employees():
    worker = worker_dao.get_all_employees()
    assert len(worker) > 0


# successfully retrieved worker by worker_id
def test_get_user_by_id():
    worker = worker_dao.get_worker_by_id(1)
    assert worker.worker_id == 1


# failed to get worker by worker id because not exist, 404
def test_get_user_by_id_fail_not_exist():
    try:
        worker = worker_dao.get_worker_by_id(4444444)
        assert False
    except WorkerNotFoundException as e:
        assert e.code == 404


# fail to get user by id because invalid input given
def test_get_user_by_id_fail_bad_values():
    try:
        worker = worker_dao.get_worker_by_id("greenblue")
        assert False
    except InvalidDataTypeException as e:
        assert e.code == 500


# successfully retrieved worker by login credentials
def test_get_user_by_user_name_and_id():
    worker = worker_dao.get_worker_by_user_name_and_password("king_henry", "password")
    assert worker.user_name == "king_henry"


# fail to retrieve worker because worker not exist, 401
def test_get_user_by_user_name_and_id_fail_no_user():
    try:
        worker = worker_dao.get_worker_by_user_name_and_password("king_henryvvv", "password")
        assert False
    except InvalidLoginException as e:
        assert e.code == 401


# fail to retrieve worker because invalid password, 401
def test_get_user_by_user_name_and_id_fail_wrong_pass():
    try:
        worker = worker_dao.get_worker_by_user_name_and_password("king_henry", "password123")
        assert False
    except InvalidLoginException as e:
        assert e.code == 401


# fail to get user by id because invalid input given
def test_get_user_by_id_and_password_fail_bad_values():
    try:
        worker = worker_dao.get_worker_by_user_name_and_password(5, "password123")
        assert False
    except InvalidDataTypeException as e:
        assert e.code == 500