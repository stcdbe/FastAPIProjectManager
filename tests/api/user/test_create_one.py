from secrets import choice, token_urlsafe
from uuid import UUID

import orjson
import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient

from src.domain.user.entities.enums import UserGender
from src.presentation.user.schemas import UserCreateScheme


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
        password=token_urlsafe(16),
        first_name=token_urlsafe(16),
        second_name=token_urlsafe(16),
        gender=choice(tuple(UserGender)),
        company=token_urlsafe(16),
        join_date=None,
        job_title=token_urlsafe(16),
        date_of_birth=None,
    )

    res = await client.post(
        url,
        json=data.model_dump(mode="json"),
        headers=auth_token_headers,
    )
    assert res.status_code == status.HTTP_201_CREATED

    res_json = orjson.loads(res.content)
    assert UUID(res_json["guid"])
