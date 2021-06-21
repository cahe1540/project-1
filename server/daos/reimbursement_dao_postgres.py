import time

from entities.reimbursement import Reimbursement
from daos.reimbursement_dao import ReimbursementDAO
from exceptions.check_violation_error import CheckViolationError
from exceptions.reimbursement_not_found_error import ReimbursementNotFoundException
from exceptions.worker_not_found_error import WorkerNotFoundException
from exceptions.invalid_data_type import InvalidDataTypeException
from utils.connection import connection
import psycopg2


class ReimbursementDAOPostgres(ReimbursementDAO):
    def create_reimbursement(self, reimbursement: Reimbursement) -> Reimbursement:
        try:
            sql = """insert into reimbursement values(default, %s, %s, %s, %s, %s, %s, NULL, NULL) returning *"""
            cursor = connection.cursor()
            now = int(round(time.time()*1000))
            cursor.execute(sql, (now, reimbursement.amount, reimbursement.reason, "pending", reimbursement.file, reimbursement.employee_id))
            connection.commit()
            record = cursor.fetchone()
            return Reimbursement(*record)
        except psycopg2.errors.CheckViolation as e:
            connection.rollback()
            raise CheckViolationError("An input argument failed a table constraint", str(e), 400)
        except psycopg2.errors.ForeignKeyViolation as e:
            connection.rollback()
            raise WorkerNotFoundException(f"Employee with id {reimbursement.employee_id} does not exist.", str(e), 404)

    def get_all_reimbursements(self) -> list[Reimbursement]:
        sql = """select * from reimbursement"""
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        records = cursor.fetchall()
        reimbursement_list = [Reimbursement(*record) for record in records]
        return reimbursement_list

    def get_reimbursements_by_employee_id(self, employee_id: int) -> list[Reimbursement]:
        if not isinstance(employee_id, int):
            raise InvalidDataTypeException("employee_id must be of type int!", "", 500)
        sql = """select * from reimbursement where employee_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, (employee_id,))
        records = cursor.fetchall()
        reimbursement_list = [Reimbursement(*record) for record in records]
        return reimbursement_list

    def update_reimbursement_by_id(self, reimbursement_id: int, manager_id: int, changes: tuple) -> Reimbursement:
        if type(reimbursement_id) != int or type(changes[0]) != str or type(changes[1]) != str or type (manager_id) != int:
            raise InvalidDataTypeException("reimbursement_id and manager_id must be of type int, and values in changes = (str, str)", "", 400)
        try:
            sql = """update reimbursement set state = %s, manager_message = %s, manager_id = %s where 
            reimbursement_id = %s returning * """
            cursor = connection.cursor()
            cursor.execute(sql, (*changes, manager_id, reimbursement_id))
            connection.commit()
            record = cursor.fetchone()
            return Reimbursement(*record)
        except psycopg2.errors.CheckViolation as e:
            connection.rollback()
            raise CheckViolationError("An input argument failed a table constraint", str(e), 400)
        except TypeError as e:
            raise ReimbursementNotFoundException(f"Reimbursement with id {reimbursement_id} does not exist.", str(e), 404)
        except psycopg2.errors.ForeignKeyViolation as e:
            connection.rollback()
            raise WorkerNotFoundException(f"Manager with id {manager_id} does not exist.", str(e), 404)

    def delete_reimbursement(self, reimbursement_id: int) -> Reimbursement:
        try:
            sql = """delete from reimbursement where reimbursement_id = %s returning *"""
            cursor = connection.cursor()
            cursor.execute(sql, (reimbursement_id,))
            connection.commit()
            deleted_record = cursor.fetchone()
            return Reimbursement(*deleted_record)
        except TypeError as e:
            raise ReimbursementNotFoundException(f"Reimbursement with id {reimbursement_id} does not exist.", str(e), 404)
