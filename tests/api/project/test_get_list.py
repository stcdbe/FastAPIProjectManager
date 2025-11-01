import orjson
import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient


@pytest.mark.asyncio(loop_scope="session")
async def test_get_project_list(
    app: FastAPI,
    client: AsyncClient,
    auth_token_headers: dict[str, str],
) -> None:
    url = app.url_path_for("get_project_list")

    res = await client.get(url, headers=auth_token_headers)
    assert res.status_code == status.HTTP_200_OK

    res_json = orjson.loads(res.content)
    prjects = res_json["projects"]
    assert isinstance(prjects, list)

    for project in prjects:
        assert project["title"]
