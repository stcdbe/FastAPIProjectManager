from abc import ABC, abstractmethod
from typing import Any

from src.modules.user.models.entities import User


class AbstractUserRepository(ABC):
    @abstractmethod
    async def get_list(self, limit: int, offset: int, order_by: str, reverse: bool = False) -> list[User]: ...

    @abstractmethod
    async def get_one(self, **kwargs: Any) -> User | None: ...

    @abstractmethod
    async def create_one(self, user: User) -> User: ...

    @abstractmethod
    async def patch_one(self, user: User) -> User: ...
