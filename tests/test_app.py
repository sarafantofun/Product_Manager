import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from fastapi import status
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.api.db.models import Base
from main import app
from tests.test_db_settings import TEST_DATABASE_URL


test_engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)
test_session = async_sessionmaker(test_engine, expire_on_commit=False)


Base.metadata.bind = test_engine


@pytest_asyncio.fixture
async def async_test_session():
    """Creation an asynchronous session for tests"""
    async with test_session() as session:
        yield session


@pytest_asyncio.fixture(autouse=True, scope="session")
async def a_prepare_database():
    """Before testing, clears the test db. After clearing, tables are created"""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield


@pytest_asyncio.fixture(scope="function")
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_create_product_success(async_test_session, async_client):
    """Successful POST request"""
    response = await async_client.post(
        "/api/product/",
        json={"title": "Bread", "price": 135.18, "count": 3},
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        "message": "Product created successfully",
        "product": {
            "title": "Bread",
            "price": 135.18,
            "count": 3,
            "id": 1
        }
    }


# @pytest.mark.asyncio
# async def test_create_product_negative_price():
#     # POST request with negative_price
#     async with AsyncClient(app=app, base_url="http://test") as ac:
#         response = await ac.post(
#             "/api/product/",
#             json={"title": "Bread", "price": -135.18, "count": 3},
#         )
#         assert response.status_code == status.HTTP_400_BAD_REQUEST
#         assert response.json()["detail"] == "Price must be non-negative"
#
#
# @pytest.mark.asyncio
# async def test_add_product_missing_title():
#     # POST request with missing required field
#     async with AsyncClient(app=app, base_url="http://test") as ac:
#         response = await ac.post(
#             "/api/product/",
#             json={"title": "Bread", "count": 5},
#         )
#         assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
#         assert response.json()["detail"][0]["msg"] == "field required"
#
#
# @pytest.mark.asyncio
# async def test_add_product_invalid_price_type():
#     # POST request with invalid price type
#     async with AsyncClient(app=app, base_url="http://test") as ac:
#         response = await ac.post(
#             "/api/product/",
#             json={"title": "Bread", "price": "135.18", "count": 3},
#         )
#     assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
#     assert response.json()["detail"][0]["msg"] == "value is not a valid float"
#
#new_product_id = response.json()["product"]["id"]
# response = await ac.get("/api/product/")
# response = await client.get(f"/api/users/{new_user_id}/")
# assert response.status_code == status.HTTP_200_OK
# assert len(response.json()["data"]) == 1