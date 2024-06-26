from http import HTTPStatus

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio(scope="session")
async def test_create_token(client: AsyncClient) -> None:
    data = {
        "username": "auth_username",
        "email": "auth_email@example.com",
        "password": "passwordpassword",
    }
    await client.post("/api/v1/users", json=data)

    auth_form_data = {"username": "auth_username", "password": "passwordpassword"}
    res = await client.post("/api/v1/auth/create_token", data=auth_form_data)
    token = res.json()
    assert res.status_code == HTTPStatus.CREATED
    assert token
    assert token["access_token"]
    assert token["refresh_token"]


@pytest.mark.asyncio(scope="session")
async def test_refresh_token(client: AsyncClient) -> None:
    data = {"username": "auth_username", "password": "passwordpassword"}
    res = await client.post("/api/v1/auth/create_token", data=data)
    token = res.json()

    res = await client.post("/api/v1/auth/refresh_token", params={"token": token["refresh_token"]})
    new_token = res.json()
    assert res.status_code == HTTPStatus.CREATED
    assert new_token
    assert new_token["access_token"]
