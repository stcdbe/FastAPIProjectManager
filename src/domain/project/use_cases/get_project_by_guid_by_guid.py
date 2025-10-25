from uuid import UUID

from src.domain.project.entities.project import Project
from src.services.project_service import ProjectService


class GetProjectByGUIDUseCase:
    __slots__ = ("_project_service",)

    def __init__(self) -> None:
        self._project_service = ProjectService()

    async def execute(self, guid: UUID) -> Project:
        return await self._project_service.get_one_by_guid(guid)
