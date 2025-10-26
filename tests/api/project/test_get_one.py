from uuid import uuid4

import orjson
import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient

from tests.mock_data import MOCK_PROJECT_GET_GUID


@pytest.mark.asyncio
async def test_get_project(
    app: FastAPI,
    client: AsyncClient,
    auth_token_headers: dict[str, str],
) -> None:
    url = app.url_path_for("get_project", project_guid=str(MOCK_PROJECT_GET_GUID))

    res = await client.get(url, headers=auth_token_headers)
    assert res.status_code == status.HTTP_200_OK

    res_json = orjson.loads(res.content)
    assert res_json["title"]


@pytest.mark.asyncio
async def test_get_project_failed(
    app: FastAPI,
    client: AsyncClient,
    auth_token_headers: dict[str, str],
) -> None:
    url = app.url_path_for("get_project", project_guid=str(uuid4()))

    res = await client.get(url, headers=auth_token_headers)
    assert res.status_code == status.HTTP_404_NOT_FOUND
