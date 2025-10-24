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

    token = orjson.loads(res.content)
    assert token["access_token"]
    assert token["refresh_token"]
    assert token["token_type"] == "bearer"  # noqa: S105
