from fastapi import Request
from fastapi.responses import JSONResponse

from app.errors.models import ErrorResponse


async def custom_exception_handlerA(request: Request, exc: ErrorResponse):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})


async def custom_exception_handlerB(request: Request, exc: ErrorResponse):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})
