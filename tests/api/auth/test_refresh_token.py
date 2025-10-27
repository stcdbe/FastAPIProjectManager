from secrets import token_urlsafe

import orjson
import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient

from src.presentation.auth.schemas import RefreshTokenInputScheme


@pytest.mark.asyncio
async def test_refresh_token(
    app: FastAPI,
    client: AsyncClient,
    auth_token_headers: dict[str, str],
) -> None:
    create_access_token_url = app.url_path_for("create_token")
    auth_form_data = {
        "username": "auth_username",
        "password": "passwordpassword",
    }
    create_access_token_res = await client.post(create_access_token_url, data=auth_form_data)
    create_access_token_res_json = orjson.loads(create_access_token_res.content)

    data = RefreshTokenInputScheme(refresh_token=create_access_token_res_json["refresh_token"])
    refresh_token_url = app.url_path_for("refresh_token")
    refresh_token_res = await client.post(refresh_token_url, json=data.model_dump(), headers=auth_token_headers)
    assert refresh_token_res.status_code == status.HTTP_201_CREATED

    res_json = orjson.loads(refresh_token_res.content)
    assert res_json["access_token"]
    assert res_json["refresh_token"]
    assert res_json["token_type"] == "bearer"  # noqa: S105


@pytest.mark.asyncio
async def test_refresh_token_failed_with_invalid_token(
    app: FastAPI,
    client: AsyncClient,
    auth_token_headers: dict[str, str],
) -> None:
    data = RefreshTokenInputScheme(refresh_token=token_urlsafe(16))
    refresh_token_url = app.url_path_for("refresh_token")
    refresh_token_res = await client.post(refresh_token_url, json=data.model_dump(), headers=auth_token_headers)
    assert refresh_token_res.status_code == status.HTTP_400_BAD_REQUEST
