from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.task.entities.task import Task


class AbstractTaskRepository(ABC):
    @abstractmethod
    async def get_list_by_project_guid(self, project_guid: UUID) -> list[Task]: ...
    @abstractmethod
    async def get_one_by_guid(self, guid: UUID) -> Task: ...
    @abstractmethod
    async def create_one(self, task: Task) -> UUID: ...
    @abstractmethod
    async def patch_one(self, task: Task) -> UUID: ...
    @abstractmethod
    async def delete_one(self, task: Task) -> UUID: ...
