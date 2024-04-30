from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.config import settings
from src.core.models.base import SQLAlchemyBaseModel

test_async_engine = create_async_engine(
    url=settings.PG_URL_TEST,
    echo=False,
    pool_pre_ping=True,
    pool_size=10,
    pool_recycle=3600,
)

test_async_session_factory = async_sessionmaker(bind=test_async_engine, expire_on_commit=False)


async def get_test_session() -> AsyncGenerator[AsyncSession, None]:
    async with test_async_session_factory() as test_session:
        yield test_session


async def create_tables() -> None:
    async with test_async_engine.begin() as conn:
        await conn.run_sync(SQLAlchemyBaseModel.metadata.create_all)


async def drop_tables() -> None:
    async with test_async_engine.begin() as conn:
        await conn.run_sync(SQLAlchemyBaseModel.metadata.drop_all)
