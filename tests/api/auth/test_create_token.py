from secrets import token_urlsafe

import orjson
import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_token(
    app: FastAPI,
    client: AsyncClient,
) -> None:
    url = app.url_path_for("create_token")
    auth_form_data = {
        "username": "auth_username",
        "password": "passwordpassword",
    }

    res = await client.post(url, data=auth_form_data)
    assert res.status_code == status.HTTP_201_CREATED

    res_json = orjson.loads(res.content)
    assert res_json["access_token"]
    assert res_json["refresh_token"]
    assert res_json["token_type"] == "bearer"  # noqa: S105


@pytest.mark.asyncio
async def test_create_token_failed_with_invalid_form_data(
    app: FastAPI,
    client: AsyncClient,
) -> None:
    url = app.url_path_for("create_token")
    auth_form_data = {
        "username": token_urlsafe(16),
        "password": token_urlsafe(16),
    }

    res = await client.post(url, data=auth_form_data)
    assert res.status_code == status.HTTP_401_UNAUTHORIZED
