from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession


from app.api.db import get_db_session
from app.api.schemas import Product as ProductCreate
from app.api.db.models.products import Product as DBProduct
from app.errors.exceptions import CustomExceptionA, CustomExceptionB

router = APIRouter(prefix="/product", tags=["Product"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_product(
    data: ProductCreate,
    db: AsyncSession = Depends(get_db_session),
):
    db_product = DBProduct(title=data.title, price=data.price, count=data.count)
    db.add(db_product)
    await db.commit()
    return db_product


@router.get("/{product_id}")
async def get_product(product_id: int, db: AsyncSession = Depends(get_db_session)):
    result = await db.execute(select(DBProduct).filter(DBProduct.id == product_id))
    product_obj = result.scalars().first()
    if product_obj is None:
        raise CustomExceptionA(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product for get not found"
        )
    return product_obj


@router.put("/{product_id}")
async def update_product(
    product_id: int,
    data: ProductCreate,
    db: AsyncSession = Depends(get_db_session),
):
    result = await db.execute(select(DBProduct).filter(DBProduct.id == product_id))
    product_obj_update = result.scalars().first()
    if product_obj_update is None:
        raise CustomExceptionB(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product for update not found"
        )
    product_obj_update.title = data.title
    product_obj_update.price = data.price
    product_obj_update.count = data.count
    await db.commit()
    return product_obj_update


@router.delete("/{product_id}")
async def del_product(
    product_id: int,
    db: AsyncSession = Depends(get_db_session),
):
    result = await db.execute(select(DBProduct).filter(DBProduct.id == product_id))
    product_to_delete = result.scalars().first()
    if product_to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    await db.delete(product_to_delete)
    await db.commit()
    return {
        "message": f"Product successfully deleted",
    }
