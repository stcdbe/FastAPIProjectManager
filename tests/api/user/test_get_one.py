from uuid import uuid4

import orjson
import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient

from tests.mock_data import MOCK_USER_GET_GUID


@pytest.mark.asyncio(loop_scope="session")
async def test_get_user(
    app: FastAPI,
    client: AsyncClient,
    auth_token_headers: dict[str, str],
) -> None:
    url = app.url_path_for("get_user", user_guid=str(MOCK_USER_GET_GUID))

    res = await client.get(url, headers=auth_token_headers)
    assert res.status_code == status.HTTP_200_OK

    res_json = orjson.loads(res.content)
    assert res_json["username"]
    assert res_json["email"]
    assert res_json.get("password") is None


@pytest.mark.asyncio(loop_scope="session")
async def test_get_user_failed_with_non_existing_user(
    app: FastAPI,
    client: AsyncClient,
    auth_token_headers: dict[str, str],
) -> None:
    url = app.url_path_for("get_user", user_guid=str(uuid4()))

    res = await client.get(url, headers=auth_token_headers)
    assert res.status_code == status.HTTP_404_NOT_FOUND
