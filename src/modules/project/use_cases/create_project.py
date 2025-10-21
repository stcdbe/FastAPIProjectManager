from uuid import UUID

from src.modules.project.entities.project import ProjectCreateData
from src.modules.project.services.project_service import ProjectService
from src.modules.user.entities.user import User


class CreateProjectUseCase:
    def __init__(self) -> None:
        self._project_service = ProjectService()

    async def execute(self, creator: User, project_create_data: ProjectCreateData) -> UUID:
        return await self._project_service.create_one(project_create_data)
