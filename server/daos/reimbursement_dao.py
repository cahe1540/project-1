from abc import ABC, abstractmethod
from entities.reimbursement import Reimbursement


class ReimbursementDAO(ABC):
    @abstractmethod
    def create_reimbursement(self, reimbursement: Reimbursement) -> Reimbursement:
        pass

    @abstractmethod
    def get_all_reimbursements(self) -> list[Reimbursement]:
        pass

    @abstractmethod
    def get_reimbursements_by_employee_id(self, employee_id) -> list[Reimbursement]:
        pass

    @abstractmethod
    def update_reimbursement_by_id(self, reimbursement_id: int, manager_id: int, changes: tuple) -> Reimbursement:
        pass

    @abstractmethod
    def delete_reimbursement(self, reimbursement_id: int) -> Reimbursement:
        pass