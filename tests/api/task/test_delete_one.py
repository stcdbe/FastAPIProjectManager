from uuid import uuid4

import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient

from tests.mock_data import MOCK_PROJECT_GET_GUID, MOCK_TASK_DELETE_GUID


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_task(
    app: FastAPI,
    client: AsyncClient,
    auth_token_headers: dict[str, str],
) -> None:
    url = app.url_path_for(
        "delete_task",
        project_guid=str(MOCK_PROJECT_GET_GUID),
        task_guid=str(MOCK_TASK_DELETE_GUID),
    )

    res = await client.delete(url, headers=auth_token_headers)
    assert res.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_task_failed_with_non_existing_project(
    app: FastAPI,
    client: AsyncClient,
    auth_token_headers: dict[str, str],
) -> None:
    url = app.url_path_for(
        "delete_task",
        project_guid=str(uuid4()),
        task_guid=str(MOCK_TASK_DELETE_GUID),
    )

    res = await client.delete(url, headers=auth_token_headers)
    assert res.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_task_failed_with_non_existing_task(
    app: FastAPI,
    client: AsyncClient,
    auth_token_headers: dict[str, str],
) -> None:
    url = app.url_path_for(
        "delete_task",
        project_guid=str(MOCK_PROJECT_GET_GUID),
        task_guid=str(uuid4()),
    )

    res = await client.delete(url, headers=auth_token_headers)
    assert res.status_code == status.HTTP_404_NOT_FOUND
