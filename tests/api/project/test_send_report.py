import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient

from src.presentation.project.schemas import ProjectReportSendDataScheme
from tests.mock_data import MOCK_PROJECT_GET_GUID


@pytest.mark.asyncio
async def test_send_project_report(
    app: FastAPI,
    client: AsyncClient,
    auth_token_headers: dict[str, str],
) -> None:
    url = app.url_path_for("send_project_report")
    data = ProjectReportSendDataScheme(
        project_guid=MOCK_PROJECT_GET_GUID,
        email="test@email.com",
    )

    res = await client.post(
        url,
        json=data.model_dump(mode="json"),
        headers=auth_token_headers,
    )
    assert res.status_code == status.HTTP_202_ACCEPTED
