from abc import ABC, abstractmethod
from uuid import UUID

from src.modules.user.entities.user import User


class AbstractUserRepository(ABC):
    @abstractmethod
    async def get_list(
        self,
        offset: int,
        limit: int,
        order_by: str,
        reverse: bool,
    ) -> list[User]: ...
    @abstractmethod
    async def get_one_by_guid(self, guid: UUID) -> User: ...
    @abstractmethod
    async def get_one_by_username(self, username: str) -> User: ...
    @abstractmethod
    async def create_one(self, user: User) -> UUID: ...
    @abstractmethod
    async def patch_one(self, user: User) -> UUID: ...
