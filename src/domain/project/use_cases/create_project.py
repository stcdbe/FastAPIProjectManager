from uuid import UUID

from src.domain.project.entities.project import ProjectCreateData
from src.domain.user.entities.user import User
from src.services.project_service import ProjectService


class CreateProjectUseCase:
    def __init__(self) -> None:
        self._project_service = ProjectService()

    async def execute(self, creator: User, project_create_data: ProjectCreateData) -> UUID:
        return await self._project_service.create_one(project_create_data)
