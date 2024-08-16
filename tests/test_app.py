from asyncio import new_event_loop

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
async_test_session_factory = async_sessionmaker(test_engine, expire_on_commit=False)


Base.metadata.bind = test_engine


@pytest.fixture(scope="session")
def event_loop():
    """Creates a new event loop for all tests"""
    loop = new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def async_test_session():
    """Creation an asynchronous session for tests"""
    async with async_test_session_factory() as session:
        yield session


@pytest_asyncio.fixture(autouse=True, scope="function")
async def init_db():
    """Before testing, clears the test db. After clearing, tables are created"""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        yield


@pytest_asyncio.fixture(scope="function")
async def async_client():
    """A fixture for creating an asynchronous HTTP client"""
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test",
    ) as client:
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
            "description": ""
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
    """Successful GET request get product by id"""
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
        "description": ""
    }


@pytest.mark.asyncio
async def test_get_product_not_found(async_test_session, async_client):
    """GET request with not found product id"""
    response = await async_client.get(
        "/api/product/100000000/"
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["message"] == "Product not found"


@pytest.mark.asyncio
async def test_update_product_success(async_test_session, async_client):
    """Successful PUT request"""
    response = await async_client.post(
        "/api/product/",
        json={"title": "Bread", "price": 135.18, "count": 3, "description": ""},
    )
    new_product_id = response.json()["product"]["id"]
    response = await async_client.put(
        f"/api/product/{new_product_id}/",
        json={
            "title": "Tasty bread",
            "price": 150.00,
            "count": 10,
            "description": "The best bread in the city"
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": new_product_id,
        "title": "Tasty bread",
        "price": 150.00,
        "count": 10,
        "description": "The best bread in the city"
    }
