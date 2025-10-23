import orjson
import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient


@pytest.mark.asyncio(scope="session")
async def test_create_access_token(
    app: FastAPI,
    client: AsyncClient,
) -> None:
    url = app.url_path_for("create_access_token")
    auth_form_data = {
        "username": "auth_username",
        "password": "passwordpassword",
    }

    res = await client.post(url, data=auth_form_data)
    assert res.status_code == status.HTTP_201_CREATED

    token = orjson.loads(res.content)
    assert token["access_token"]
    assert token["refresh_token"]
    assert token["token_type"] == "Bearer"  # noqa: S105


@pytest.mark.asyncio(scope="session")
async def test_refresh_access_token(
    app: FastAPI,
    client: AsyncClient,
    auth_token_headers: dict[str, str],
) -> None:
    url = app.url_path_for("refresh_access_token")
    res = await client.post(url, headers=auth_token_headers)
    assert res.status_code == status.HTTP_201_CREATED

    token = orjson.loads(res.content)
    assert token["access_token"]
    assert token["refresh_token"]
    assert token["token_type"] == "Bearer"  # noqa: S105
