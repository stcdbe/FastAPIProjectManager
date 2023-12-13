from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.config import PG_URL


async_engine = create_async_engine(url=PG_URL,
                                   echo=False,
                                   pool_pre_ping=True,
                                   pool_size=10,
                                   pool_recycle=3600)

async_session = async_sessionmaker(bind=async_engine,
                                   expire_on_commit=False,
                                   class_=AsyncSession)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
