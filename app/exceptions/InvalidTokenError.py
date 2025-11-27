from fastapi import HTTPException


class InvalidTokenError(HTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=403, detail=message)
