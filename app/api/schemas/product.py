from pydantic import BaseModel


class Product(BaseModel):
    title: str
    price: float
    count: int
