from datetime import UTC, datetime
from uuid import UUID

import orjson
import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient

from src.domain.user.enums import UserGender
from src.presentation.user.schemas import UserPatchScheme
from tests.sqlalchemy import MOCK_USER_PATCH_GUID


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

    res = await client.patch(
        url,
        json=data.model_dump(mode="json"),
        headers=auth_token_headers,
    )
    assert res.status_code == status.HTTP_200_OK

    res_json = orjson.loads(res.content)
    assert UUID(res_json["guid"])
