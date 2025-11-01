from uuid import UUID

import orjson
import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient

from tests.mock_data import MOCK_PROJECT_GET_GUID


@pytest.mark.asyncio(loop_scope="session")
async def test_get_task_list(
    app: FastAPI,
    client: AsyncClient,
    auth_token_headers: dict[str, str],
) -> None:
    url = app.url_path_for(
        "get_task_list",
        project_guid=str(MOCK_PROJECT_GET_GUID),
    )

    res = await client.get(url, headers=auth_token_headers)
    assert res.status_code == status.HTTP_200_OK

    res_json = orjson.loads(res.content)
    tasks = res_json["tasks"]
    assert isinstance(tasks, list)

    for task in tasks:
        assert UUID(task["guid"])
        assert task["created_at"]
        assert task["updated_at"]
        assert task["title"]
