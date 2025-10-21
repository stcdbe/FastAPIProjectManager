from uuid import UUID

from src.modules.project.entities.project import ProjectCreateData
from src.modules.user.entities.user import User


class CreateProjectUseCase:
    async def execute(self, creator: User, create_project_data: ProjectCreateData) -> UUID: ...
