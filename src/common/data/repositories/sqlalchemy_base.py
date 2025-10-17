from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

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


class SQLAlchemyRepository:
    _session: AsyncSession

    def __init__(self, session: Annotated[AsyncSession, Depends(get_session)]) -> None:
        self._session = session
