from datetime import datetime, timedelta

import pytest
from httpx import AsyncClient

from src.config import settings


@pytest.mark.asyncio(scope="session")
async def test_get_some_projects(client: AsyncClient) -> None:
    res = await client.get("/api/v1/projects")
    assert res.status_code == 200


@pytest.mark.asyncio(scope="session")
async def test_create_project(client: AsyncClient, user_token_headers: dict[str, str]) -> None:
    data = {
        "title": "test_title",
        "description": "test_description",
        "tech_stack": ["string"],
        "start_date": (datetime.utcnow() + timedelta(days=1)).isoformat(),
        "constraint_date": (datetime.utcnow() + timedelta(days=365)).isoformat(),
        "mentor_guid": None,
    }
    res = await client.post("/api/v1/projects", json=data, headers=user_token_headers)
    project = res.json()
    assert res.status_code == 201
    assert project
    assert project["guid"]
    assert project["created_at"]
    assert project["updated_at"]
    for key, val in data.items():
        assert project[key] == val


@pytest.mark.asyncio(scope="session")
async def test_get_project(client: AsyncClient, test_project_guid: str) -> None:
    res = await client.get(f"/api/v1/projects/{test_project_guid}")
    project = res.json()
    assert res.status_code == 200
    assert project
    assert project["guid"] == test_project_guid


@pytest.mark.asyncio(scope="session")
async def test_patch_project(
    client: AsyncClient,
    test_user_guid: str,
    test_project_guid: str,
    user_token_headers: dict[str, str],
) -> None:
    data = {
        "title": "test_patch_title",
        "description": "test_patch_description",
        "tech_stack": ["patch_string"],
        "start_date": (datetime.utcnow() + timedelta(days=1)).isoformat(),
        "constraint_date": (datetime.utcnow() + timedelta(days=365)).isoformat(),
        "mentor_guid": test_user_guid,
    }
    res = await client.patch(
        f"/api/v1/projects/{test_project_guid}",
        json=data,
        headers=user_token_headers,
    )
    upd_project = res.json()
    assert res.status_code == 200
    assert upd_project
    for key, val in data.items():
        assert upd_project[key] == val


@pytest.mark.asyncio(scope="session")
async def test_create_project_task(
    client: AsyncClient,
    test_user_guid: str,
    test_project_guid: str,
    user_token_headers: dict[str, str],
) -> None:
    test_task_data = {
        "title": "test_title",
        "description": "test_description",
        "is_completed": False,
        "executor_guid": test_user_guid,
    }
    res = await client.post(
        f"/api/v1/projects/{test_project_guid}",
        json=test_task_data,
        headers=user_token_headers,
    )
    project = res.json()
    assert res.status_code == 201
    assert project
    assert test_task_data["title"] in {task["title"] for task in project["tasks"]}
    assert test_task_data["description"] in {task["description"] for task in project["tasks"]}
    assert test_task_data["executor_guid"] in {task["executor_guid"] for task in project["tasks"]}


@pytest.mark.asyncio(scope="session")
async def test_patch_project_task(
    client: AsyncClient,
    test_project_guid: str,
    test_task_guid: str,
    user_token_headers: dict[str, str],
) -> None:
    test_patch_task_data = {
        "title": "test_patch_title",
        "description": "test_patch_description",
        "is_completed": True,
        "executor_guid": None,
    }
    res = await client.patch(
        f"/api/v1/projects/{test_project_guid}/tasks/{test_task_guid}",
        json=test_patch_task_data,
        headers=user_token_headers,
    )
    project = res.json()
    assert res.status_code == 200
    assert project
    assert test_patch_task_data["title"] in {task["title"] for task in project["tasks"]}
    assert test_patch_task_data["description"] in {task["description"] for task in project["tasks"]}


@pytest.mark.asyncio(scope="session")
async def test_del_project_task(
    client: AsyncClient,
    test_project_guid: str,
    test_task_guid: str,
    user_token_headers: dict[str, str],
) -> None:
    res = await client.delete(
        f"/api/v1/projects/{test_project_guid}/tasks/{test_task_guid}",
        headers=user_token_headers,
    )
    assert res.status_code == 204


@pytest.mark.asyncio(scope="session")
async def test_send_project_report(
    client: AsyncClient, test_project_uuid: str, user_token_headers: dict[str, str]
) -> None:
    res = await client.post(
        f"/api/projects/{test_project_uuid}/send_as_report/{settings.TEST_EMAIL_RECEIVER}",
        headers=user_token_headers,
    )
    assert res.status_code == 202


@pytest.mark.asyncio(scope="session")
async def test_del_project(
    client: AsyncClient,
    test_project_guid: str,
    user_token_headers: dict[str, str],
) -> None:
    res = await client.delete(f"/api/v1/projects/{test_project_guid}", headers=user_token_headers)
    assert res.status_code == 204
