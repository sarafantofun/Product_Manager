from fastapi import APIRouter

from .endpoints.auth import router as auth_router
from .endpoints.product import router as product_router
from .endpoints.users import router as user_router

router = APIRouter(prefix="/api")

router.include_router(product_router)
router.include_router(auth_router)
router.include_router(user_router)
