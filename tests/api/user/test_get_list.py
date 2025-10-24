import orjson
import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient


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
