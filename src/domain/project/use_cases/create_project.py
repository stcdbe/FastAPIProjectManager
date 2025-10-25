from uuid import UUID

from src.domain.project.entities import ProjectCreateData
from src.domain.user.entities import User
from src.services.project_service import ProjectService


class CreateProjectUseCase:
    __slots__ = ("_project_service",)

    def __init__(self) -> None:
        self._project_service = ProjectService()

    async def execute(self, creator: User, project_create_data: ProjectCreateData) -> UUID:
        return await self._project_service.create_one(creator.guid, project_create_data)
