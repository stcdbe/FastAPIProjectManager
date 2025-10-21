from uuid import UUID

from src.modules.project.entities.project import Project


class GetProjectByGUIDUseCase:
    async def execute(self, guid: UUID) -> Project: ...
