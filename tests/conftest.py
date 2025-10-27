from collections.abc import AsyncGenerator

import pytest_asyncio

from tests.mock_data import mock_project_entities, mock_task_entities, mock_user_entities
from tests.sql import create_sql_tables, drop_sql_tables, insert_mock_sql_data


@pytest_asyncio.fixture(autouse=True, scope="session")
async def prepare_sql_db() -> AsyncGenerator[None, None]:
    await drop_sql_tables()
    await create_sql_tables()
    await insert_mock_sql_data(mock_user_entities, mock_project_entities, mock_task_entities)
    yield
    await drop_sql_tables()
