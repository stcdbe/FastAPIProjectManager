from abc import ABC, abstractmethod
from typing import Any

from src.modules.project.models.entities import Project


class AbstractProjectRepository(ABC):
    @abstractmethod
    async def get_list(self, limit: int, offset: int, order_by: str, reverse: bool = False) -> list[Project]: ...

    @abstractmethod
    async def get_one(self, **kwargs: Any) -> Project | None: ...

    @abstractmethod
    async def create_one(self, project: Project) -> Project: ...

    @abstractmethod
    async def patch_one(self, project: Project) -> Project: ...

    @abstractmethod
    async def del_one(self, project: Project) -> None: ...
