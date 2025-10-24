import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient

from tests.sqlalchemy import MOCK_PROJECT_DELETE_GUID


@pytest.mark.asyncio
async def test_delete_project(
    app: FastAPI,
    client: AsyncClient,
    auth_token_headers: dict[str, str],
) -> None:
    url = app.url_path_for("delete_project", project_guid=str(MOCK_PROJECT_DELETE_GUID))

    res = await client.delete(url, headers=auth_token_headers)
    assert res.status_code == status.HTTP_204_NO_CONTENT
