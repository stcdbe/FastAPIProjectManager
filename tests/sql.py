from collections.abc import AsyncGenerator, Iterable
from contextlib import asynccontextmanager
from dataclasses import asdict
from typing import Any

import orjson
from psycopg import AsyncConnection
from psycopg.types.json import Jsonb

from src.config import get_settings
from src.domain.project.entities import Project
from src.domain.task.entities import Task
from src.domain.user.entities import User

_DROP_USER_TABLE_SQL = """DROP TABLE IF EXISTS "user" CASCADE;"""
_DROP_USER_EMAIL_INDEX_SQL = """DROP INDEX IF EXISTS ix_user_email;"""
_DROP_USER_USERNAME_INDEX_SQL = """DROP INDEX IF EXISTS ix_user_username;"""
_DROP_PROJECT_TABLE_SQL = """DROP TABLE IF EXISTS "project" CASCADE;"""
_DROP_TASK_TABLE_SQL = """DROP TABLE IF EXISTS "task" CASCADE;"""

_CREATE_USER_TABLE_SQL = """CREATE TABLE "user" (
    username VARCHAR(128) NOT NULL,
    email VARCHAR(128) NOT NULL,
    password VARCHAR(128) NOT NULL,
    first_name VARCHAR(64),
    second_name VARCHAR(64),
    gender VARCHAR(1),
    company VARCHAR(128),
    join_date DATE,
    job_title VARCHAR(128),
    date_of_birth DATE,
    is_deleted BOOLEAN NOT NULL,
    deleted_at TIMESTAMP WITHOUT TIME ZONE,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    guid UUID NOT NULL,
    CONSTRAINT pk_user PRIMARY KEY (guid)
);"""
_CREATE_USER_EMAIL_INDEX_SQL = """CREATE UNIQUE INDEX ix_user_email ON "user" (email);"""
_CREATE_USER_USERNAME_INDEX_SQL = """CREATE UNIQUE INDEX ix_user_username ON "user" (username);"""
_CREATE_PROJECT_TABLE_SQL = """CREATE TABLE "project" (
    title VARCHAR(256) NOT NULL,
    description TEXT NOT NULL,
    tech_stack VARCHAR[] NOT NULL,
    additional_metadata JSONB NOT NULL,
    start_date DATE NOT NULL,
    constraint_date DATE NOT NULL,
    creator_guid UUID NOT NULL,
    mentor_guid UUID,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    guid UUID NOT NULL,
    CONSTRAINT pk_project PRIMARY KEY (guid),
    CONSTRAINT fk_project_creator_guid_user FOREIGN KEY(creator_guid) REFERENCES "user" (guid),
    CONSTRAINT fk_project_mentor_guid_user FOREIGN KEY(mentor_guid) REFERENCES "user" (guid)
);"""
_CREATE_TASK_TABLE_SQL = """CREATE TABLE "task" (
    title VARCHAR(256) NOT NULL,
    description TEXT NOT NULL,
    is_completed BOOLEAN NOT NULL,
    project_guid UUID NOT NULL,
    executor_guid UUID NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    guid UUID NOT NULL,
    CONSTRAINT pk_task PRIMARY KEY (guid),
    CONSTRAINT fk_task_executor_guid_user FOREIGN KEY(executor_guid) REFERENCES "user" (guid),
    CONSTRAINT fk_task_project_guid_project FOREIGN KEY(project_guid) REFERENCES "project" (guid)
);"""

_INSERT_USER_DATA_SQL = """INSERT INTO "user" (
    guid,
    username,
    email,
    password,
    first_name,
    second_name,
    gender,
    company,
    join_date,
    job_title,
    date_of_birth,
    is_deleted,
    deleted_at,
    created_at,
    updated_at
) VALUES (
    %(guid)s,
    %(username)s,
    %(email)s,
    %(password)s,
    %(first_name)s,
    %(second_name)s,
    %(gender)s,
    %(company)s,
    %(join_date)s,
    %(job_title)s,
    %(date_of_birth)s,
    %(is_deleted)s,
    %(deleted_at)s,
    %(created_at)s,
    %(updated_at)s
);"""

_INSERT_PROJECT_DATA_SQL = """INSERT INTO "project" (
    guid,
    title,
    description,
    tech_stack,
    additional_metadata,
    start_date,
    constraint_date,
    creator_guid,
    mentor_guid,
    created_at,
    updated_at
) VALUES (
    %(guid)s,
    %(title)s,
    %(description)s,
    %(tech_stack)s,
    %(additional_metadata)s,
    %(start_date)s,
    %(constraint_date)s,
    %(creator_guid)s,
    %(mentor_guid)s,
    %(created_at)s,
    %(updated_at)s
);"""

_INSERT_TAKS_DATA_SQL = """INSERT INTO "task" (
    guid,
    title,
    description,
    is_completed,
    project_guid,
    executor_guid,
    created_at,
    updated_at
) VALUES (
    %(guid)s,
    %(title)s,
    %(description)s,
    %(is_completed)s,
    %(project_guid)s,
    %(executor_guid)s,
    %(created_at)s,
    %(updated_at)s
);"""


@asynccontextmanager
async def get_pg_conn() -> AsyncGenerator[AsyncConnection, None]:
    host, *_ = get_settings().PG_URL_TEST.hosts()
    *_, db = get_settings().PG_URL_TEST.unicode_string().split("/")
    async with await AsyncConnection.connect(
        f"dbname={db} user={host['username']} password={host['password']} host={host['host']} port={host['port']}",
    ) as conn:
        yield conn


async def create_sql_tables(conn: AsyncConnection) -> None:
    async with conn.cursor() as cur:
        await cur.execute(_CREATE_USER_TABLE_SQL)
        await cur.execute(_CREATE_USER_USERNAME_INDEX_SQL)
        await cur.execute(_CREATE_USER_EMAIL_INDEX_SQL)
        await cur.execute(_CREATE_PROJECT_TABLE_SQL)
        await cur.execute(_CREATE_TASK_TABLE_SQL)


async def drop_sql_tables(conn: AsyncConnection) -> None:
    async with conn.cursor() as cur:
        await cur.execute(_DROP_TASK_TABLE_SQL)
        await cur.execute(_DROP_PROJECT_TABLE_SQL)
        await cur.execute(_DROP_USER_USERNAME_INDEX_SQL)
        await cur.execute(_DROP_USER_EMAIL_INDEX_SQL)
        await cur.execute(_DROP_USER_TABLE_SQL)


def _modyfy_project_dict_for_insertion(
    project: dict[str, Any],
) -> dict[str, Any]:
    project["tech_stack"] = list(project["tech_stack"])
    project["additional_metadata"] = Jsonb(project["additional_metadata"], orjson.dumps)
    return project


async def insert_mock_sql_data(
    conn: AsyncConnection,
    mock_users: Iterable[User],
    mock_projects: Iterable[Project],
    mock_tasks: Iterable[Task],
) -> None:
    async with conn.cursor() as cur:
        await cur.executemany(_INSERT_USER_DATA_SQL, (asdict(entity) for entity in mock_users))
        await cur.executemany(
            _INSERT_PROJECT_DATA_SQL,
            (_modyfy_project_dict_for_insertion(asdict(entity)) for entity in mock_projects),
        )
        await cur.executemany(_INSERT_TAKS_DATA_SQL, (asdict(entity) for entity in mock_tasks))
