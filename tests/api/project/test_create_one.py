from datetime import UTC, datetime, timedelta
from secrets import token_urlsafe
from uuid import UUID, uuid4

import orjson
import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient

from src.presentation.project.schemas import ProjectCreateScheme


@pytest.mark.asyncio
async def test_create_project(
    app: FastAPI,
    client: AsyncClient,
    auth_token_headers: dict[str, str],
) -> None:
    url = app.url_path_for("create_project")
    data = ProjectCreateScheme(
        title="create_title",
        description=token_urlsafe(16),
        tech_stack={token_urlsafe(16), token_urlsafe(16)},
        additional_metadata={"meta": token_urlsafe(16)},
        start_date=datetime.now(UTC).date() + timedelta(days=365),
        constraint_date=datetime.now(UTC).date() + timedelta(days=365),
        mentor_guid=None,
    )

    res = await client.post(
        url,
        json=data.model_dump(mode="json"),
        headers=auth_token_headers,
    )
    assert res.status_code == status.HTTP_201_CREATED

    res_json = orjson.loads(res.content)
    assert UUID(res_json["guid"])


@pytest.mark.asyncio
async def test_create_project_failed(
    app: FastAPI,
    client: AsyncClient,
    auth_token_headers: dict[str, str],
) -> None:
    url = app.url_path_for("create_project")
    data = ProjectCreateScheme(
        title="create_title",
        description=token_urlsafe(16),
        tech_stack={token_urlsafe(16), token_urlsafe(16)},
        additional_metadata={"meta": token_urlsafe(16)},
        start_date=datetime.now(UTC).date() + timedelta(days=365),
        constraint_date=datetime.now(UTC).date() + timedelta(days=365),
        mentor_guid=uuid4(),
    )

    res = await client.post(
        url,
        json=data.model_dump(mode="json"),
        headers=auth_token_headers,
    )
    assert res.status_code == status.HTTP_400_BAD_REQUEST
