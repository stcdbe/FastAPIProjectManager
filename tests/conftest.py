from collections.abc import AsyncGenerator
from datetime import UTC, datetime, timedelta
from typing import TypedDict
from uuid import uuid4

import orjson
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient

from src.main import create_app
from tests.sqlalchemy import create_tables, drop_tables

mock_user_guid = uuid4()
mock_project_guid = uuid4()
mock_task_guid = uuid4()

mock_data_for_tests = {
    "user": {
        "guid": mock_user_guid,
        "username": "auth_username",
        "email": "auth_email@example.com",
        "password": "passwordpassword",
    },
    "project": {
        "guid": mock_project_guid,
        "title": "project_title",
        "description": "project_description",
        "tech_stack": ["string1"],
        "start_date": (datetime.now(UTC) + timedelta(days=1)).isoformat(),
        "constraint_date": (datetime.now(UTC) + timedelta(days=365)).isoformat(),
        "mentor_guid": None,
    },
    "task": {
        "guid": mock_task_guid,
        "title": "task_title",
        "description": "task_description",
        "is_completed": False,
        "executor_guid": mock_user_guid,
    },
}


class AuthTokenHeaders(TypedDict):
    Authorization: str


@pytest_asyncio.fixture(scope="session")
async def app() -> AsyncGenerator[FastAPI, None]:
    app = create_app()
    # app.dependency_overrides[get_session] = get_test_session
    yield app


@pytest_asyncio.fixture(autouse=True, scope="session")
async def prepare_test_db() -> AsyncGenerator[None, None]:
    await drop_tables()
    await create_tables()
    yield
    await drop_tables()


@pytest_asyncio.fixture(scope="session")
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as cli:
        yield cli


@pytest_asyncio.fixture(scope="session")
async def auth_token_headers(client: AsyncClient) -> AsyncGenerator[AuthTokenHeaders, None]:
    auth_data = {
        "username": "auth_username",
        "password": "passwordpassword",
    }
    res = await client.post("/api/v1/auth/create_token", data=auth_data)

    access_token = orjson.loads(res.content)["access_token"]
    yield AuthTokenHeaders(Authorization=f"Bearer {access_token}")


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
