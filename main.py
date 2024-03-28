from fastapi import FastAPI

from app.api import router
from app.errors.exceptions import (
    ProductNotFoundException,
    InvalidProductDataException,
)
from app.errors.handlers import (
    custom_not_found_exception_handler,
    custom_request_validation_exception_handler,
)

app = FastAPI()

app.include_router(router)


app.add_exception_handler(ProductNotFoundException, custom_not_found_exception_handler)
app.add_exception_handler(
    InvalidProductDataException, custom_request_validation_exception_handler
)
