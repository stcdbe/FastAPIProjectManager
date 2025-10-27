from uuid import uuid4

import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient

from tests.mock_data import MOCK_USER_DELETE_GUID


@pytest.mark.asyncio
async def test_delete_user(
    app: FastAPI,
    client: AsyncClient,
    auth_token_headers: dict[str, str],
) -> None:
    url = app.url_path_for("delete_user", user_guid=str(MOCK_USER_DELETE_GUID))

    res = await client.delete(url, headers=auth_token_headers)
    assert res.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.asyncio
async def test_delete_user_failed_with_non_existing_user(
    app: FastAPI,
    client: AsyncClient,
    auth_token_headers: dict[str, str],
) -> None:
    url = app.url_path_for("delete_user", user_guid=str(uuid4()))

    res = await client.delete(url, headers=auth_token_headers)
    assert res.status_code == status.HTTP_404_NOT_FOUND
