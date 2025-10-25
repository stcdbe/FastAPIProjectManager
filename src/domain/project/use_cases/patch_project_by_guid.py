from uuid import UUID

from src.domain.project.entities.project import ProjectPatchData
from src.services.project_service import ProjectService


class PatchProjectByGUIDUseCase:
    __slots__ = ("_project_service",)

    def __init__(self) -> None:
        self._project_service = ProjectService()

    async def execute(
        self,
        guid: UUID,
        project_patch_data: ProjectPatchData,
    ) -> UUID:
        project = await self._project_service.get_one_by_guid(guid)
        return await self._project_service.patch_one(project, project_patch_data)
