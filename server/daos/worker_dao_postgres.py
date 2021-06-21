import psycopg2

from daos.worker_dao import WorkerDAO
from entities.worker import Worker
from exceptions.invalid_login_error import InvalidLoginException
from exceptions.worker_not_found_error import WorkerNotFoundException
from exceptions.invalid_data_type import InvalidDataTypeException
from utils.connection import connection


class WorkerDAOPostgres(WorkerDAO):
    def get_all_employees(self):
        sql = """select * from worker where worker.role = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, ('employee',))
        connection.commit()
        records = cursor.fetchall()
        worker_list = [Worker(*record) for record in records]
        return worker_list

    def get_worker_by_id(self, worker_id: int):
        if type(worker_id) != int:
            raise InvalidDataTypeException(f"worker_id must be of type int", "", 500)
        try:
            sql = """select * from worker where worker_id = %s"""
            cursor = connection.cursor()
            cursor.execute(sql, (worker_id,))
            resource = cursor.fetchone()
            employee = Worker(*resource)
            return employee
        except TypeError as e:
            raise WorkerNotFoundException(f"Worker with id {worker_id} does not exist.", str(e), 404)

    def get_worker_by_user_name_and_password(self, user_name: str, password: str) -> Worker:
        if not isinstance(user_name, str) or not isinstance(password, str):
            raise InvalidDataTypeException(f"user_name must be of type str and password must be of type str", "",
                                            500)
        try:
            sql = """select * from worker where user_name = %s"""
            cursor = connection.cursor()
            cursor.execute(sql, (user_name,))
            resource = cursor.fetchone()
            worker = Worker(*resource)
            # if password does not match, raise error
            if worker.password != password:
                msg = "Password or username was incorrect, please try again."
                raise InvalidLoginException(msg, msg, 401)
            else:
                return worker
        except TypeError as e:
            msg = "Password or username was incorrect, please try again."
            raise InvalidLoginException(msg, msg, 401)