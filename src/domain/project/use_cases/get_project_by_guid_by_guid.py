from uuid import UUID

from src.domain.project.entities import Project
from src.services.project_service import ProjectService


class GetProjectByGUIDUseCase:
    __slots__ = ("_project_service",)

    def __init__(self, project_service: ProjectService) -> None:
        self._project_service = project_service

    async def execute(self, guid: UUID) -> Project:
        return await self._project_service.get_one_by_guid(guid)
