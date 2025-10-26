from uuid import UUID

from src.services.project_service import ProjectService


class DeleteProjectByGUIDUseCase:
    __slots__ = ("_project_service",)

    def __init__(self, project_service: ProjectService) -> None:
        self._project_service = project_service

    async def execute(self, guid: UUID) -> UUID:
        project = await self._project_service.get_one_by_guid(guid)
        return await self._project_service.delete_one(project)
