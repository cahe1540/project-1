from abc import ABC, abstractmethod
from entities.worker import Worker


class WorkerDAO(ABC):
    @abstractmethod
    def get_all_employees(self):
        pass

    @abstractmethod
    def get_worker_by_id(self, worker_id: int):
        pass

    @abstractmethod
    def get_worker_by_user_name_and_password(self, user_name: str, password: str) -> Worker:
        pass
