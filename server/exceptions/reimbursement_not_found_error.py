class ReimbursementNotFoundException(Exception):
    def __init__(self, summary: str, message: str, code: int):
        self.summary = summary
        self.message = message
        self.code = code
