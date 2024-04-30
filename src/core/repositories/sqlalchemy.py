from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.sqlalchemy import get_session


class SQLAlchemyRepository:
    _session: AsyncSession

    def __init__(self, session: Annotated[AsyncSession, Depends(get_session)]) -> None:
        self._session = session
