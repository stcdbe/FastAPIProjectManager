from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.project.entities import Project


class AbstractProjectRepository(ABC):
    @abstractmethod
    async def get_list(
        self,
        limit: int,
        offset: int,
        order_by: str,
        reverse: bool,
    ) -> list[Project]: ...
    @abstractmethod
    async def get_one_by_guid(self, guid: UUID) -> Project: ...
    @abstractmethod
    async def create_one(self, project: Project) -> UUID: ...
    @abstractmethod
    async def patch_one(self, project: Project) -> UUID: ...
    @abstractmethod
    async def delete_one(self, project: Project) -> UUID: ...
