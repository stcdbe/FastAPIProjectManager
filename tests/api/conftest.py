from collections.abc import AsyncGenerator

import orjson
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from src.main import create_app, lifespan
from tests.sqlalchemy import insert_mock_data

# , drop_tables, insert_mock_data


@pytest_asyncio.fixture(scope="session")
async def app() -> AsyncGenerator[FastAPI, None]:
    app = create_app()
    # app.dependency_overrides[get_session] = get_test_session
    async with lifespan(app):
        yield app


@pytest_asyncio.fixture(autouse=True, scope="session")
async def prepare_test_db() -> AsyncGenerator[None, None]:
    # await drop_tables()
    # await create_tables()
    await insert_mock_data()
    # test_broker = TestRabbitBroker(broker, with_real=True)
    # await test_broker
    yield
    # await test_broker
    # await drop_tables()


@pytest_asyncio.fixture(scope="session")
async def client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as cli:
        yield cli


@pytest_asyncio.fixture(scope="session")
async def auth_token_headers(
    app: FastAPI,
    client: AsyncClient,
) -> AsyncGenerator[dict[str, str], None]:
    auth_data = {
        "username": "auth_username",
        "password": "passwordpassword",
    }
    url = app.url_path_for("create_token")
    res = await client.post(url, data=auth_data)

    access_token = orjson.loads(res.content)["access_token"]
    yield {"Authorization": f"Bearer {access_token}"}
