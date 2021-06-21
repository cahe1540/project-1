from abc import ABC, abstractmethod

from entities.worker import Worker
from entities.reimbursement import Reimbursement


class AppServices(ABC):
    @abstractmethod
    def add_reimbursement(self, reimbursement: Reimbursement) -> Reimbursement:
        pass

    @abstractmethod
    def retrieve_all_reimbursements(self) -> list[Reimbursement]:
        pass

    @abstractmethod
    def retrieve_reimbursements_by_employee_id(self, employee_id: int) -> list[Reimbursement]:
        pass

    @abstractmethod
    def retrieve_worker_by_user_name_and_password(self, user_name: str, password: str) -> Worker:
        pass

    @abstractmethod
    def retrieve_all_employees(self):
        pass

    @abstractmethod
    def update_reimbursement_by_id(self, reimbursement_id: int, manager_id: int, changes: tuple) -> Reimbursement:
        pass

    @abstractmethod
    def delete_own_reimbursement_by_id(self, reimbursement_id: int, employee_id: int) -> Reimbursement:
        pass
