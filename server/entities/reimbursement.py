class Reimbursement:
    def __init__(self, reimbursement_id: int,created_at: int, amount: int, reason: str, state: str, file: str,
                 employee_id: int, manager_id: int, manager_message: str):
        self.reimbursement_id = reimbursement_id
        self.created_at = created_at
        self.amount = amount
        self.reason = reason
        self.state = state
        self.file = file
        self.employee_id = employee_id
        self.manager_id = manager_id
        self.manager_message = manager_message

    def as_json_dict(self):
        return {
            "reimbursementId": self.reimbursement_id,
            "createdAt": self.created_at,
            "amount": float(self.amount),
            "reason": self.reason,
            "state": self.state,
            "file": self.file,
            "employeeId": self.employee_id,
            "managerId": self.manager_id,
            "managerMessage": self.manager_message
        }
