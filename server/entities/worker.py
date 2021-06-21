class Worker:
    def __init__(self, worker_id: int, first_name: str, last_name: str, user_name: str, image: str, password: str, role: str):
        self.worker_id = worker_id
        self.first_name = first_name
        self.last_name = last_name
        self.user_name = user_name
        self.image = image
        self.password = password
        self.role = role

    def as_json_dict(self):
        return {
            "workerId": self.worker_id,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "userName": self.user_name,
            "image": self.image,
            "role": self.role
        }
