from collections.abc import AsyncGenerator

import orjson
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from src.main import create_app
from tests.sqlalchemy import create_tables, drop_tables, insert_mock_data


@pytest_asyncio.fixture(scope="session")
async def app() -> AsyncGenerator[FastAPI, None]:
    app = create_app()
    # app.dependency_overrides[get_session] = get_test_session
    yield app


@pytest_asyncio.fixture(autouse=True, scope="session")
async def prepare_test_db() -> AsyncGenerator[None, None]:
    await drop_tables()
    await create_tables()
    await insert_mock_data()
    yield
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


# @pytest_asyncio.fixture(scope="session")
# async def test_user_guid(client: AsyncClient, user_token_headers: AuthTokenHeaders) -> str:
#     res = await client.get("/api/v1/users/me", headers=user_token_headers)
#     return orjson.loads(res.content)["guid"]


# @pytest_asyncio.fixture(scope="session")
# async def test_project_guid(client: AsyncClient, user_token_headers: AuthTokenHeaders) -> str:
#     data = {
#         "title": "project_title",
#         "description": "project_description",
#         "tech_stack": ["string1"],
#         "start_date": (datetime.now(UTC) + timedelta(days=1)).isoformat(),
#         "constraint_date": (datetime.now(UTC) + timedelta(days=365)).isoformat(),
#         "mentor_guid": None,
#     }
#     res = await client.post("/api/v1/projects", json=data, headers=user_token_headers)
#     return orjson.loads(res.content)["guid"]


# @pytest_asyncio.fixture(scope="session")
# async def test_task_guid(
#     client: AsyncClient,
#     user_token_headers: AuthTokenHeaders,
#     test_user_guid: str,
#     test_project_guid: str,
# ) -> str:
#     data = {
#         "title": "task_title",
#         "description": "task_description",
#         "is_completed": False,
#         "executor_guid": test_user_guid,
#     }
#     res = await client.post(
#         f"/api/v1/projects/{test_project_guid}",
#         json=data,
#         headers=user_token_headers,
#     )
#     project = orjson.loads(res.content)
#     project_tasks = project["tasks"]
#     return project_tasks[0]["guid"]
