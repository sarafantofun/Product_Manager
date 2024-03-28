from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.errors.exceptions import InvalidProductDataException
from app.errors.models import ErrorResponseModel


async def custom_not_found_exception_handler(request: Request, exc: ErrorResponseModel):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail, "error": str(exc)},
    )


async def custom_request_validation_exception_handler(
    request: Request,
    exc: InvalidProductDataException,
):
    return JSONResponse(
        status_code=exc.body.get("status_code", status.HTTP_400_BAD_REQUEST),
        content=exc.body,
    )
