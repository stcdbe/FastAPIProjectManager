from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.common.data.models.sqlalchemy_base import SQLAlchemyBaseModel
from src.config import get_settings

async_engine = create_async_engine(
    url=get_settings().PG_URL.unicode_string(),
    echo=False,
    pool_pre_ping=True,
    pool_size=10,
    pool_recycle=3600,
)

async_session_factory = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session


async def create_tables() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLAlchemyBaseModel.metadata.create_all)


async def drop_tables() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLAlchemyBaseModel.metadata.drop_all)


class SQLAlchemyRepository:
    _session: AsyncSession

    def __init__(self, session: Annotated[AsyncSession, Depends(get_session)]) -> None:
        self._session = session
