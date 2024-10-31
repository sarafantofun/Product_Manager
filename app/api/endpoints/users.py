from fastapi import APIRouter, Depends
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.db import get_db_session
from app.api.schemas import User as UserCreate
from app.api.db.models import User as DBUser

router = APIRouter(prefix="/users", tags=["Users"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


@router.post("/create_user")
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db_session)):
    hashed_password = get_password_hash(user.password)
    db_user = DBUser(username=user.username, password=hashed_password, role=user.role)
    db.add(db_user)
    await db.commit()
    return db_user
