# returns input args as a dict to return the body nicely formatted to client
def json_response(message: str, status: int, data=None) -> dict:
    if data is not None:
        return {
            "message": message,
            "status": status,
            "data": [data]
        }
    else:
        return {
            "message": message,
            "status": status
        }