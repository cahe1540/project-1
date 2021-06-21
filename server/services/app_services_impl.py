from services.app_services import AppServices
from entities.worker import Worker
from entities.reimbursement import Reimbursement
from daos.reimbursement_dao import ReimbursementDAO
from daos.worker_dao_postgres import WorkerDAO
from exceptions.unauthorized_action_error import UnauthorizedActionException
from exceptions.worker_not_found_error import WorkerNotFoundException


class AppServicesImpl(AppServices):
    def __init__(self, workerDao: WorkerDAO, reimbursementDao: ReimbursementDAO):
        self.workerDao = workerDao
        self.reimbursementDao = reimbursementDao

    def retrieve_all_employees(self):
        return self.workerDao.get_all_employees()

    def add_reimbursement(self, reimbursement: Reimbursement) -> Reimbursement:
        # 1) add a reimbursement, if fail, dao raises error
        return self.reimbursementDao.create_reimbursement(reimbursement)

    def retrieve_all_reimbursements(self) -> list[Reimbursement]:
        # 1) get all reimbursements, if fail, dao raises error
        return self.reimbursementDao.get_all_reimbursements()

    def retrieve_reimbursements_by_employee_id(self, employee_id: int) -> list[Reimbursement]:
        # 1) check if employee exists, if not exists, workerDao raises error
        self.workerDao.get_worker_by_id(employee_id)

        # 2) get all reimbursements
        return self.reimbursementDao.get_reimbursements_by_employee_id(employee_id)

    def update_reimbursement_by_id(self, reimbursement_id: int, manager_id: int, changes: tuple) -> Reimbursement:
        # 1) update, if fail, dao raises error
        return self.reimbursementDao.update_reimbursement_by_id(reimbursement_id, manager_id, changes)

    def retrieve_worker_by_user_name_and_password(self, user_name: str, password: str) -> Worker:
        # 1) update, if fail, dao raises error
        return self.workerDao.get_worker_by_user_name_and_password(user_name, password)

    def delete_own_reimbursement_by_id(self, reimbursement_id: int, employee_id: int) -> Reimbursement:
        # 1) check if employee exists
        employee = self.workerDao.get_worker_by_id(employee_id)
        if not employee:
            raise WorkerNotFoundException(f"Employee with id: {employee_id} does not exist.", "404 not found", 404)

        # 2) check if reimbursement belongs to employee_id
        reimbursements: list[Reimbursement] = self.reimbursementDao.get_reimbursements_by_employee_id(employee_id)
        ids = [reimbursement.employee_id for reimbursement in reimbursements]
        if employee_id not in ids:
            raise UnauthorizedActionException("You cannot delete reimbursements that don't belong to you.", "Unauthorized", 401)

        # 2) delete reimbursement, dao raises errors if not exist
        return self.reimbursementDao.delete_reimbursement(reimbursement_id)