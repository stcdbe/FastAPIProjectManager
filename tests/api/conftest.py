from collections.abc import AsyncGenerator

import orjson
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from src.logic.api_di_container import get_api_di_container
from src.main import create_app
from tests.logic.mock_api_di_container import get_mock_api_di_container


@pytest_asyncio.fixture(scope="session")
async def app() -> AsyncGenerator[FastAPI, None]:
    app = create_app()
    app.dependency_overrides[get_api_di_container] = get_mock_api_di_container
    yield app


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
