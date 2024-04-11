from abc import ABC

from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import SQLAlchemySessionDep


class SQLAlchemyRepository(ABC):
    session: AsyncSession

    def __init__(self, session: SQLAlchemySessionDep) -> None:
        self.session = session
