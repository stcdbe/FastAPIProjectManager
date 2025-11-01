from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.user.entities import User


class AbstractUserCacheRepository(ABC):
    @abstractmethod
    async def add_one(self, user: User) -> None: ...
    @abstractmethod
    async def get_one(self, guid: UUID) -> User | None: ...
    @abstractmethod
    async def delete_one(self, guid: UUID) -> None: ...
