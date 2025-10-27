from logging import getLogger
from uuid import UUID

from src.domain.project.entities import ProjectCreateData
from src.services.project_service import ProjectService

logger = getLogger()


class CreateProjectUseCase:
    __slots__ = ("_project_service",)

    def __init__(self, project_service: ProjectService) -> None:
        self._project_service = project_service

    async def execute(self, creator_guid: UUID, project_create_data: ProjectCreateData) -> UUID:
        logger.info("Creating project %s", project_create_data.title)
        return await self._project_service.create_one(creator_guid, project_create_data)
