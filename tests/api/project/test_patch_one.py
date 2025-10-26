from datetime import UTC, datetime, timedelta
from secrets import token_urlsafe
from uuid import UUID, uuid4

import orjson
import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient

from src.presentation.project.schemas import ProjectPatchScheme
from tests.mock_data import MOCK_PROJECT_PATCH_GUID


@pytest.mark.asyncio
async def test_patch_project(
    app: FastAPI,
    client: AsyncClient,
    auth_token_headers: dict[str, str],
) -> None:
    url = app.url_path_for("patch_project", project_guid=str(MOCK_PROJECT_PATCH_GUID))
    data = ProjectPatchScheme(
        title=None,
        description=token_urlsafe(16),
        tech_stack={token_urlsafe(16), token_urlsafe(16)},
        additional_metadata={},
        start_date=datetime.now(UTC).date() + timedelta(days=1),
        constraint_date=datetime.now(UTC).date() + timedelta(days=10),
        mentor_guid=None,
    )

    res = await client.patch(
        url,
        json=data.model_dump(mode="json"),
        headers=auth_token_headers,
    )
    assert res.status_code == status.HTTP_200_OK

    res_json = orjson.loads(res.content)
    assert UUID(res_json["guid"])


@pytest.mark.asyncio
async def test_patch_project_failed(
    app: FastAPI,
    client: AsyncClient,
    auth_token_headers: dict[str, str],
) -> None:
    url = app.url_path_for("patch_project", project_guid=str(uuid4()))
    data = ProjectPatchScheme(
        title=None,
        description=token_urlsafe(16),
        tech_stack={token_urlsafe(16), token_urlsafe(16)},
        additional_metadata={},
        start_date=datetime.now(UTC).date() + timedelta(days=1),
        constraint_date=datetime.now(UTC).date() + timedelta(days=10),
        mentor_guid=None,
    )

    res = await client.patch(
        url,
        json=data.model_dump(mode="json"),
        headers=auth_token_headers,
    )
    assert res.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_patch_project_with_invalid_mentor_guid(
    app: FastAPI,
    client: AsyncClient,
    auth_token_headers: dict[str, str],
) -> None:
    url = app.url_path_for("patch_project", project_guid=str(MOCK_PROJECT_PATCH_GUID))
    data = ProjectPatchScheme(
        title=None,
        description=token_urlsafe(16),
        tech_stack={token_urlsafe(16), token_urlsafe(16)},
        additional_metadata={},
        start_date=datetime.now(UTC).date() + timedelta(days=1),
        constraint_date=datetime.now(UTC).date() + timedelta(days=10),
        mentor_guid=uuid4(),
    )

    res = await client.patch(
        url,
        json=data.model_dump(mode="json"),
        headers=auth_token_headers,
    )
    assert res.status_code == status.HTTP_400_BAD_REQUEST
