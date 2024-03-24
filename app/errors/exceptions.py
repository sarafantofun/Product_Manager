from fastapi import HTTPException


class CustomExceptionA(HTTPException):
    def __init__(self, detail: str = "Exception from A", status_code: int = 400):
        super().__init__(status_code=status_code, detail=detail)


class CustomExceptionB(HTTPException):
    def __init__(self, detail: str = "Exception from B", status_code: int = 401):
        super().__init__(status_code=status_code, detail=detail)
