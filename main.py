from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError

from app.api import router
from app.errors.exceptions import CustomExceptionA, CustomExceptionB
from app.errors.handlers import (
    custom_exception_handlerA,
    custom_exception_handlerB,
    custom_http_exception_handler,
    custom_request_validation_exception_handler,
)

app = FastAPI()

app.include_router(router)

app.add_exception_handler(CustomExceptionA, custom_exception_handlerA)
app.add_exception_handler(CustomExceptionB, custom_exception_handlerB)
app.add_exception_handler(HTTPException, custom_http_exception_handler)
app.add_exception_handler(
    RequestValidationError, custom_request_validation_exception_handler
)
