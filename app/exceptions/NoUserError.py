from fastapi import HTTPException


class NoUserError(HTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=401, detail=message)
