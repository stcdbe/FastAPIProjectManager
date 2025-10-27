from secrets import token_urlsafe
from uuid import UUID, uuid4

import orjson
import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient

from src.presentation.task.schemas import TaskPatchScheme
from tests.mock_data import MOCK_PROJECT_GET_GUID, MOCK_TASK_PATCH_GUID, MOCK_USER_GET_GUID


@pytest.mark.asyncio
async def test_patch_task(
    app: FastAPI,
    client: AsyncClient,
    auth_token_headers: dict[str, str],
) -> None:
    url = app.url_path_for(
        "patch_task",
        project_guid=str(MOCK_PROJECT_GET_GUID),
        task_guid=str(MOCK_TASK_PATCH_GUID),
    )
    data = TaskPatchScheme(
        title="patch_title",
        description=token_urlsafe(16),
        is_completed=True,
        executor_guid=MOCK_USER_GET_GUID,
    )

    res = await client.patch(url, headers=auth_token_headers, json=data.model_dump(mode="json"))
    assert res.status_code == status.HTTP_200_OK

    res_json = orjson.loads(res.content)
    assert UUID(res_json["guid"])


@pytest.mark.asyncio
async def test_patch_task_failed_with_non_existing_project(
    app: FastAPI,
    client: AsyncClient,
    auth_token_headers: dict[str, str],
) -> None:
    url = app.url_path_for(
        "patch_task",
        project_guid=str(uuid4()),
        task_guid=str(MOCK_TASK_PATCH_GUID),
    )
    data = TaskPatchScheme(
        title="patch_title",
        description=token_urlsafe(16),
        is_completed=True,
        executor_guid=None,
    )

    res = await client.patch(url, headers=auth_token_headers, json=data.model_dump(mode="json"))
    assert res.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_patch_task_failed_with_non_existing_task(
    app: FastAPI,
    client: AsyncClient,
    auth_token_headers: dict[str, str],
) -> None:
    url = app.url_path_for(
        "patch_task",
        project_guid=str(MOCK_PROJECT_GET_GUID),
        task_guid=str(uuid4()),
    )
    data = TaskPatchScheme(
        title="patch_title",
        description=token_urlsafe(16),
        is_completed=True,
        executor_guid=None,
    )

    res = await client.patch(url, headers=auth_token_headers, json=data.model_dump(mode="json"))
    assert res.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_patch_task_failed_with_non_existing_executor(
    app: FastAPI,
    client: AsyncClient,
    auth_token_headers: dict[str, str],
) -> None:
    url = app.url_path_for(
        "patch_task",
        project_guid=str(MOCK_PROJECT_GET_GUID),
        task_guid=str(MOCK_TASK_PATCH_GUID),
    )
    data = TaskPatchScheme(
        title="patch_title",
        description=token_urlsafe(16),
        is_completed=True,
        executor_guid=uuid4(),
    )

    res = await client.patch(url, headers=auth_token_headers, json=data.model_dump(mode="json"))
    assert res.status_code == status.HTTP_400_BAD_REQUEST
