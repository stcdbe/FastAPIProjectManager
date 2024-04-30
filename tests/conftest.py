from datetime import datetime, timedelta
from typing import AsyncGenerator

import pytest_asyncio
from httpx import AsyncClient

from src.core.database.sqlalchemy import get_session
from src.main import app
from tests.sqlalchemy import create_tables, drop_tables, get_test_session

app.dependency_overrides[get_session] = get_test_session


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
async def user_token_headers(client: AsyncClient) -> dict[str, str]:
    data = {
        "username": "auth_username",
        "email": "auth_email@example.com",
        "password": "passwordpassword",
    }
    await client.post("/api/v1/users", json=data)

    data.pop("email")
    res = await client.post("/api/v1/auth/create_token", data=data)

    access_token = res.json()["access_token"]
    return {"Authorization": f"Bearer {access_token}"}


@pytest_asyncio.fixture(scope="session")
async def test_user_guid(client: AsyncClient, user_token_headers: dict[str, str]) -> str:
    res = await client.get("/api/v1/users/me", headers=user_token_headers)
    return res.json()["guid"]


@pytest_asyncio.fixture(scope="session")
async def test_project_guid(client: AsyncClient, user_token_headers: dict[str, str]) -> str:
    data = {
        "title": "project_title",
        "description": "project_description",
        "tech_stack": ["string1"],
        "start_date": (datetime.utcnow() + timedelta(days=1)).isoformat(),
        "constraint_date": (datetime.utcnow() + timedelta(days=365)).isoformat(),
        "mentor_guid": None,
    }
    res = await client.post("/api/v1/projects", json=data, headers=user_token_headers)
    return res.json()["guid"]


@pytest_asyncio.fixture(scope="session")
async def test_task_guid(
    client: AsyncClient,
    user_token_headers: dict[str, str],
    test_user_guid: str,
    test_project_guid: str,
) -> str:
    data = {
        "title": "task_title",
        "description": "task_description",
        "is_completed": False,
        "executor_guid": test_user_guid,
    }
    res = await client.post(
        f"/api/v1/projects/{test_project_guid}",
        json=data,
        headers=user_token_headers,
    )
    project = res.json()
    project_tasks = project["tasks"]
    return project_tasks[0]["guid"]
