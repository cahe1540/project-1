from utils.json_response import json_response
from exceptions.check_violation_error import CheckViolationError
from exceptions.invalid_login_error import InvalidLoginException
from exceptions.invalid_data_type import InvalidDataTypeException
from exceptions.reimbursement_not_found_error import ReimbursementNotFoundException
from exceptions.unauthorized_action_error import UnauthorizedActionException
from exceptions.worker_not_found_error import WorkerNotFoundException


# handle possible exceptions in this app
def handle_exceptions(route_handler):
    def handler(*args, **kwargs):
        try:
            return route_handler(*args, **kwargs)
        except CheckViolationError as e:
            return json_response(e.summary, e.code), e.code
        except InvalidDataTypeException as e:
            return json_response(e.summary, e.code), e.code
        except InvalidLoginException as e:
            return json_response(e.summary, e.code), e.code
        except ReimbursementNotFoundException as e:
            return json_response(e.summary, e.code), e.code
        except UnauthorizedActionException as e:
            return json_response(e.summary, e.code), e.code
        except WorkerNotFoundException as e:
            return json_response(e.summary, e.code), e.code
        except TypeError as e:
            return json_response(str(e), 400), 400
        except ValueError as e:
            return json_response(str(e), 404), 404
        except LookupError as e:
            return json_response(str(e), 400), 400
        except Exception as e:
            return json_response(str(e), 500), 500
    handler.__name__ = route_handler.__name__
    return handler
