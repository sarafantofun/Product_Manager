from fastapi import Request
from fastapi.responses import JSONResponse

from app.errors.models import ErrorResponse


async def custom_exception_handlerA(request: Request, exc: ErrorResponse):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})


async def custom_exception_handlerB(request: Request, exc: ErrorResponse):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})


async def custom_http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": str(exc)},
    )


async def custom_request_validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"message": "Custom Request Validation Error", "errors": exc.errors()},
    )
