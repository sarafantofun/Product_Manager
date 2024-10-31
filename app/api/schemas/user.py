from enum import Enum

from pydantic import BaseModel


class UserRole(str, Enum):
    admin = "admin"
    user = "user"
    guest = "guest"


class User(BaseModel):
    username: str
    password: str
    role: UserRole
