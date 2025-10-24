from collections.abc import AsyncGenerator
from datetime import UTC, datetime, timedelta
from secrets import token_urlsafe
from typing import Final
from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.config import get_settings
from src.data.models.project.project_model import ProjectModel
from src.data.models.sqlalchemy_base import SQLAlchemyBaseModel
from src.data.models.user.user_model import UserModel
from src.services.hasher_service import Hasher

test_async_engine = create_async_engine(
    url=get_settings().PG_URL_TEST.unicode_string(),
    echo=False,
    pool_pre_ping=True,
    pool_size=10,
    pool_recycle=3600,
)

test_async_session_factory = async_sessionmaker(
    bind=test_async_engine,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


async def get_test_session() -> AsyncGenerator[AsyncSession, None]:
    async with test_async_session_factory() as test_session:
        yield test_session


async def create_tables() -> None:
    async with test_async_engine.begin() as conn:
        await conn.run_sync(SQLAlchemyBaseModel.metadata.create_all)


async def drop_tables() -> None:
    async with test_async_engine.begin() as conn:
        await conn.run_sync(SQLAlchemyBaseModel.metadata.drop_all)


MOCK_USER_AUTH_GUID: Final[UUID] = uuid4()
MOCK_USER_GET_GUID: Final[UUID] = uuid4()
MOCK_USER_PATCH_GUID: Final[UUID] = uuid4()
MOCK_USER_DELETE_GUID: Final[UUID] = uuid4()

MOCK_PROJECT_GET_GUID: Final[UUID] = uuid4()
MOCK_PROJECT_PATCH_GUID: Final[UUID] = uuid4()
MOCK_PROJECT_DELETE_GUID: Final[UUID] = uuid4()
# MOCK_TASK_GUID: Final[UUID] = uuid4()

mock_user_data = (
    (MOCK_USER_AUTH_GUID, "auth_username", "auth@email.com"),
    (MOCK_USER_GET_GUID, "get_username", "get@email.com"),
    (MOCK_USER_PATCH_GUID, "patch_username", "patch@email.com"),
    (MOCK_USER_DELETE_GUID, "delete_username", "delete@email.com"),
)
mock_projet_data = (
    (MOCK_PROJECT_GET_GUID, "get_title"),
    (MOCK_PROJECT_PATCH_GUID, "patch_title"),
    (MOCK_PROJECT_DELETE_GUID, "delete_title"),
)


async def insert_mock_data() -> None:
    mock_user_models = (
        UserModel(
            guid=guid,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
            username=username,
            email=email,
            password=Hasher().get_psw_hash("passwordpassword"),
            first_name=None,
            second_name=None,
            gender=None,
            company=None,
            join_date=None,
            job_title=None,
            date_of_birth=None,
            is_deleted=False,
            deleted_at=None,
        )
        for guid, username, email in mock_user_data
    )
    mock_project_models = (
        ProjectModel(
            guid=guid,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
            title=title,
            description=token_urlsafe(16),
            tech_stack=(token_urlsafe(16), token_urlsafe(16)),
            additional_metadata={},
            start_date=datetime.now(UTC).date() + timedelta(days=1),
            constraint_date=datetime.now(UTC).date() + timedelta(days=10),
            creator_guid=MOCK_USER_AUTH_GUID,
            mentor_guid=None,
        )
        for guid, title in mock_projet_data
    )
    async with test_async_session_factory() as test_session:
        test_session.add_all(mock_user_models)
        await test_session.commit()
        test_session.add_all(mock_project_models)
        await test_session.commit()
