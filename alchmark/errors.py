class APIError(Exception):
    status_code = 404

    def __init__(self, message: str, status_code: int=None):
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return {"message": self.message}