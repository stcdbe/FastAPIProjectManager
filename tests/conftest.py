from collections.abc import AsyncGenerator

import pytest_asyncio

from tests.mock_data import mock_project_entities, mock_task_entities, mock_user_entities
from tests.sql import create_sql_tables, drop_sql_tables, get_pg_conn, insert_mock_sql_data


@pytest_asyncio.fixture(autouse=True, scope="session")
async def prepare_sql_db() -> AsyncGenerator[None, None]:
    async with get_pg_conn() as conn:
        await drop_sql_tables(conn)
        await create_sql_tables(conn)
        await insert_mock_sql_data(conn, mock_user_entities, mock_project_entities, mock_task_entities)

    yield

    async with get_pg_conn() as conn:
        await drop_sql_tables(conn)
