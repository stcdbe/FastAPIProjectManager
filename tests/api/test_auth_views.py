import orjson
import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio(scope="session")
async def test_create_token(
    client: AsyncClient,
) -> None:
    auth_form_data = {"username": "auth_username", "password": "passwordpassword"}

    res = await client.post("/api/v1/auth/create_token", data=auth_form_data)
    assert res.status_code == status.HTTP_201_CREATED

    token = orjson.loads(res.content)
    assert token["access_token"]
    assert token["refresh_token"]


@pytest.mark.asyncio(scope="session")
async def test_refresh_token(client: AsyncClient, auth_token_headers: dict[str, str]) -> None:
    res = await client.post("/api/v1/auth/refresh_token", headers=auth_token_headers)
    assert res.status_code == status.HTTP_201_CREATED

    token = orjson.loads(res.content)
    assert token["access_token"]
    assert token["refresh_token"]
