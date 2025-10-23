from datetime import UTC, datetime
from uuid import UUID

import orjson
import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient

from src.domain.user.entities.enums import UserGender
from src.presentation.user.schemas import UserCreateScheme, UserPatchScheme
from tests.sqlalchemy import MOCK_USER_DELETE_GUID, MOCK_USER_GET_GUID, MOCK_USER_PATCH_GUID


@pytest.mark.asyncio
async def test_get_user_list(
    app: FastAPI,
    client: AsyncClient,
    auth_token_headers: dict[str, str],
) -> None:
    url = app.url_path_for("get_user_list")

    res = await client.get(url, headers=auth_token_headers)
    assert res.status_code == status.HTTP_200_OK

    res_json = orjson.loads(res.content)
    users = res_json["users"]
    assert isinstance(users, list)

    for user in users:
        assert user["username"]
        assert user["email"]
        assert user.get("password") is None


@pytest.mark.asyncio
async def test_create_user(
    app: FastAPI,
    client: AsyncClient,
    auth_token_headers: dict[str, str],
) -> None:
    url = app.url_path_for("create_user")
    data = UserCreateScheme(
        username="create_username",
        email="create@email.com",
        password="passwordpassword",  # noqa: S106
        first_name=None,
        second_name=None,
        gender=None,
        company=None,
        join_date=None,
        job_title=None,
        date_of_birth=None,
    )

    res = await client.post(url, json=data.model_dump(), headers=auth_token_headers)
    assert res.status_code == status.HTTP_201_CREATED

    res_json = orjson.loads(res.content)
    assert UUID(res_json["guid"])


@pytest.mark.asyncio
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


@pytest.mark.asyncio
async def test_patch_user(
    app: FastAPI,
    client: AsyncClient,
    auth_token_headers: dict[str, str],
) -> None:
    url = app.url_path_for("patch_user", user_guid=str(MOCK_USER_PATCH_GUID))
    data = UserPatchScheme(
        username=None,
        email=None,
        password=None,
        first_name="first_name",
        second_name="second_name",
        gender=UserGender.M,
        company="company",
        join_date=datetime.now(UTC).date(),
        job_title="job_title",
        date_of_birth=datetime.now(UTC).date(),
    )

    res = await client.patch(url, json=data.model_dump(), headers=auth_token_headers)
    assert res.status_code == status.HTTP_200_OK

    res_json = orjson.loads(res.content)
    assert UUID(res_json["guid"])


@pytest.mark.asyncio
async def test_delete_user(
    app: FastAPI,
    client: AsyncClient,
    auth_token_headers: dict[str, str],
) -> None:
    url = app.url_path_for("delete_user", user_guid=str(MOCK_USER_DELETE_GUID))

    res = await client.delete(url, headers=auth_token_headers)
    assert res.status_code == status.HTTP_204_NO_CONTENT
