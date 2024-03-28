from typing import Any, Sequence

from fastapi import HTTPException, status
from fastapi.exceptions import RequestValidationError

from app.errors.models import ErrorResponseModel


class ProductNotFoundException(HTTPException):
    def __init__(
        self,
        message: str = "Product not found",
        status_code: int = status.HTTP_404_NOT_FOUND,
    ):
        super().__init__(status_code=status_code, detail=message)


class InvalidProductDataException(RequestValidationError):
    def __init__(
        self,
        message: str = "Data is invalid",
        status_code: int = status.HTTP_400_BAD_REQUEST,
        errors: Sequence[Any] = None,
        body: Any = None,
    ):
        if errors is None:
            errors = [
                ErrorResponseModel(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    message="Missing required field",
                    error_code="missing_field",
                ).dict()
            ]
        if body is None:
            body = {"status_code": status_code, "detail": message, "errors": errors}

        super().__init__(errors=errors, body=body)

    def __str__(self):
        return str(self.body)
