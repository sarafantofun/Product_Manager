from fastapi import FastAPI, HTTPException

from app.api import router
from app.errors.exceptions import CustomExceptionA, CustomExceptionB
from app.errors.handlers import custom_exception_handlerA, custom_exception_handlerB

app = FastAPI()

app.include_router(router)

app.add_exception_handler(CustomExceptionA, custom_exception_handlerA)
app.add_exception_handler(CustomExceptionB, custom_exception_handlerB)
