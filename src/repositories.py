from abc import ABC, abstractmethod
from typing import Any, NoReturn

from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import SQLASessionDep


class AbstractRepository(ABC):
    @abstractmethod
    async def get_list(self, *args: Any, **kwargs: Any) -> NoReturn:
        raise NotImplementedError

    @abstractmethod
    async def get_one(self, *args: Any, **kwargs: Any) -> NoReturn:
        raise NotImplementedError

    @abstractmethod
    async def create_one(self, *args: Any, **kwargs: Any) -> NoReturn:
        raise NotImplementedError

    @abstractmethod
    async def patch_one(self, *args: Any, **kwargs: Any) -> NoReturn:
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository, ABC):
    session: AsyncSession

    def __init__(self, session: SQLASessionDep) -> None:
        self.session = session
