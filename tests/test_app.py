import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from fastapi import status
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.api.db import get_db_session
from app.api.db.models import Base
from main import app
from tests.test_db_settings import TEST_DATABASE_URL


test_engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)
async_test_session_factory = async_sessionmaker(test_engine, expire_on_commit=False)


Base.metadata.bind = test_engine


@pytest_asyncio.fixture(scope="session")
async def async_test_session():
    """Creation an asynchronous session for tests"""
    async with async_test_session_factory() as session:
        yield session


# app.dependency_overrides[get_db_session] = lambda: async_test_session()


@pytest_asyncio.fixture(autouse=True, scope="session")
async def a_prepare_database(async_test_session):
    """Before testing, clears the test db. After clearing, tables are created"""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        yield


@pytest_asyncio.fixture(scope="session")
async def async_client(async_test_session):
    """A fixture for creating an asynchronous HTTP client"""
    # transport = ASGITransport(app=app)
    # async with AsyncClient(transport=transport, base_url="http://test") as client:
    #     yield client
    def _get_test_db():
        yield async_test_session
    app.dependency_overrides[get_db_session] = _get_test_db
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
    new_product_id = response.json()["product"]["id"]
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        "message": "Product created successfully",
        "product": {
            "id": new_product_id,
            "title": "Bread",
            "price": 135.18,
            "count": 3,
            'description': ''
        }
    }


@pytest.mark.asyncio
async def test_create_product_negative_price(async_test_session, async_client):
    """POST request with negative_price"""
    response = await async_client.post(
        "/api/product/",
        json={"title": "Bread", "price": -135.18, "count": 3},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Price must be non-negative"


@pytest.mark.asyncio
async def test_add_product_missing_title(async_test_session, async_client):
    """POST request with missing required field"""
    response = await async_client.post(
        "/api/product/",
        json={"title": "Bread", "count": 5},
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()["detail"][0]["msg"] == "Field required"


@pytest.mark.asyncio
async def test_add_product_invalid_price_type(async_test_session, async_client):
    """POST request with invalid price type"""
    response = await async_client.post(
        "/api/product/",
        json={"title": "Bread", "price": "string", "count": 4},
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()["detail"][0]["msg"] == "Input should be a valid number, unable to parse string as a number"


@pytest.mark.asyncio
async def test_get_product_by_id(async_test_session, async_client):
    """Successful GET request"""
    response = await async_client.post(
        "/api/product/",
        json={"title": "Bread", "price": 135.18, "count": 3},
    )
    new_product_id = response.json()["product"]["id"]
    response = await async_client.get(f"/api/product/{new_product_id}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": new_product_id,
        "title": "Bread",
        "price": 135.18,
        "count": 3,
        'description': ''
    }


# @pytest.mark.asyncio
# async def test_get_product_not_found(async_test_session, async_client):
#     """GET request with not found product id"""
#     response = await async_client.get(
#         "/api/product/100000000/"
#     )
#     assert response.status_code == status.HTTP_404_NOT_FOUND
#     assert response.json()["message"] == "Product not found"
# response = await client.get(f"/api/users/{new_user_id}/")

# assert len(response.json()["data"]) == 1
