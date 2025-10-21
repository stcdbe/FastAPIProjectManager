from uuid import UUID

from src.modules.project.services.project_service import ProjectService


class DeleteProjectByGUIDUseCase:
    def __init__(self) -> None:
        self._project_service = ProjectService()

    async def execute(self, guid: UUID) -> UUID:
        project = await self._project_service.get_one_by_guid(guid)
        return await self._project_service.delete_one(project)
