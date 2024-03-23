from fastapi import APIRouter

from .endpoints.product import router as product_router


router = APIRouter(prefix="/api")

router.include_router(product_router)
