from collections.abc import AsyncGenerator
from datetime import UTC, datetime
from typing import Final
from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.config import get_settings
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
# MOCK_PROJECT_GUID: Final[UUID] = uuid4()
# MOCK_TASK_GUID: Final[UUID] = uuid4()


async def insert_mock_data() -> None:
    mock_models = (
        UserModel(
            guid=MOCK_USER_AUTH_GUID,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
            username="auth_username",
            email="auth@email.com",
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
        ),
        UserModel(
            guid=MOCK_USER_GET_GUID,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
            username="get_username",
            email="get@email.com",
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
        ),
        UserModel(
            guid=MOCK_USER_PATCH_GUID,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
            username="patch_username",
            email="patch@email.com",
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
        ),
        UserModel(
            guid=MOCK_USER_DELETE_GUID,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
            username="delete_username",
            email="delete@email.com",
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
        ),
    )
    async with test_async_session_factory() as test_session:
        test_session.add_all(mock_models)
        await test_session.commit()
