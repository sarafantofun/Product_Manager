from typing import Optional

from pydantic import BaseModel


class Product(BaseModel):
    title: str
    price: float
    count: int
    description: Optional[str] = None
