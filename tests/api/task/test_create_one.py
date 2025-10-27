from secrets import token_urlsafe
from uuid import UUID, uuid4

import orjson
import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient

from src.presentation.task.schemas import TaskCreateScheme
from tests.mock_data import MOCK_PROJECT_GET_GUID, MOCK_USER_AUTH_GUID


@pytest.mark.asyncio
async def test_create_task(
    app: FastAPI,
    client: AsyncClient,
    auth_token_headers: dict[str, str],
) -> None:
    url = app.url_path_for("create_task", project_guid=str(MOCK_PROJECT_GET_GUID))
    data = TaskCreateScheme(
        title="create_title",
        description=token_urlsafe(16),
        is_completed=False,
        executor_guid=MOCK_USER_AUTH_GUID,
    )

    res = await client.post(url, headers=auth_token_headers, json=data.model_dump(mode="json"))
    assert res.status_code == status.HTTP_201_CREATED

    res_json = orjson.loads(res.content)
    assert UUID(res_json["guid"])


@pytest.mark.asyncio
async def test_create_task_failed_with_non_existing_project(
    app: FastAPI,
    client: AsyncClient,
    auth_token_headers: dict[str, str],
) -> None:
    url = app.url_path_for("create_task", project_guid=str(uuid4()))
    data = TaskCreateScheme(
        title="create_title",
        description=token_urlsafe(16),
        is_completed=False,
        executor_guid=MOCK_USER_AUTH_GUID,
    )

    res = await client.post(url, headers=auth_token_headers, json=data.model_dump(mode="json"))
    assert res.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_create_task_failed_with_non_existing_executor(
    app: FastAPI,
    client: AsyncClient,
    auth_token_headers: dict[str, str],
) -> None:
    url = app.url_path_for("create_task", project_guid=str(MOCK_PROJECT_GET_GUID))
    data = TaskCreateScheme(
        title="create_title",
        description=token_urlsafe(16),
        is_completed=False,
        executor_guid=uuid4(),
    )

    res = await client.post(url, headers=auth_token_headers, json=data.model_dump(mode="json"))
    assert res.status_code == status.HTTP_400_BAD_REQUEST
