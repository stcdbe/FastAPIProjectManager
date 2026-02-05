from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from enum import StrEnum
from typing import Any

import orjson
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine


def _orjson_dumps(obj: Any) -> str:
    return orjson.dumps(obj).decode()


class PGTransactionIsolationLevel(StrEnum):
    """
    ### SERIALIZABLE
    #### Dirty Reads (seeing uncommitted data) - Prevented
    #### Non-Repeatable Reads (reading different values in same transaction) - Prevented
    #### Phantom Reads (seeing new rows in range queries) - Prevented
    Highest isolation. Guarantees that the outcome is the same as if transactions ran one after another (serially).
    Ensures full consistency but may reduce concurrency/performance.

    ### REPEATABLE READ
    #### Dirty Reads (seeing uncommitted data) - Prevented
    #### Non-Repeatable Reads (reading different values in same transaction) - Prevented
    #### Phantom Reads (seeing new rows in range queries) - Allowed (mostly)
    A transaction sees the same data for rows it has already read, even if other transactions modify those rows.
    Prevents dirty reads and non-repeatable reads.

    ### READ COMMITTED
    #### Dirty Reads (seeing uncommitted data) - Prevented
    #### Non-Repeatable Reads (reading different values in same transaction) Allowed
    #### Phantom Reads (seeing new rows in range queries) Allowed
    The default for many databases (e.g., PostgreSQL). A transaction only sees data that was committed before or during
    its execution. Prevents dirty reads.

    ### READ UNCOMMITTED
    #### Dirty Reads (seeing uncommitted data) - Allowed
    #### Non-Repeatable Reads (reading different values in same transaction) - Allowed
    #### Phantom Reads (seeing new rows in range queries) - Allowed
    Lowest isolation. A transaction can read data being modified by another uncommitted transaction. Offers high
    performance but minimal consistency.

    ### AUTOCOMMIT
    This special "isolation level" places the database connection in a non-transactional mode. SQL statements are
    executed and committed immediately without the typical BEGIN/COMMIT cycle managed by the DBAPI or SQLAlchemy.
    This mode is useful for operations that do not require transactional safety.
    """

    SERIALIZABLE = "SERIALIZABLE"
    REPEATABLE_READ = "REPEATABLE READ"
    READ_COMMITTED = "READ COMMITTED"
    READ_UNCOMMITTED = "READ UNCOMMITTED"
    AUTOCOMMIT = "AUTOCOMMIT"


class SQLAlchemyRepository:
    _read_only_engine: AsyncEngine
    _read_only_session_factory: async_sessionmaker[AsyncSession]
    _engine: AsyncEngine
    _session_factory: async_sessionmaker[AsyncSession]

    def __init__(self, pg_url: str) -> None:
        self._read_only_engine = create_async_engine(
            pg_url,
            json_serializer=_orjson_dumps,
            json_deserializer=orjson.loads,
            isolation_level=PGTransactionIsolationLevel.AUTOCOMMIT,
            pool_pre_ping=True,
            pool_size=5,
            pool_recycle=1800,
            pool_timeout=30,
            max_overflow=10,
            echo=False,
        )
        self._read_only_session_factory = async_sessionmaker(
            self._read_only_engine,
            autoflush=False,
            expire_on_commit=False,
        )
        self._engine = create_async_engine(
            pg_url,
            json_serializer=_orjson_dumps,
            json_deserializer=orjson.loads,
            isolation_level=PGTransactionIsolationLevel.READ_COMMITTED,
            pool_pre_ping=True,
            pool_size=5,
            pool_recycle=1800,
            pool_timeout=30,
            max_overflow=10,
            echo=False,
        )
        self._session_factory = async_sessionmaker(
            self._engine,
            autoflush=False,
            expire_on_commit=False,
        )

    @asynccontextmanager
    async def _get_read_only_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self._session_factory() as session:
            yield session

    @asynccontextmanager
    async def _get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self._session_factory() as session:
            yield session
