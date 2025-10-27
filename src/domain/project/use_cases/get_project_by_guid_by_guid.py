from logging import getLogger
from uuid import UUID

from src.domain.project.entities import Project
from src.services.project_service import ProjectService

logger = getLogger()


class GetProjectByGUIDUseCase:
    __slots__ = ("_project_service",)

    def __init__(self, project_service: ProjectService) -> None:
        self._project_service = project_service

    async def execute(self, project_guid: UUID) -> Project:
        logger.info("Getting one project %s", project_guid)
        return await self._project_service.get_one_by_guid(project_guid)
