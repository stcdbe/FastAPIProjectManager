from src.domain.project.entities.project import Project
from src.services.project_service import ProjectService


class GetProjectListUseCase:
    __slots__ = ("_project_service",)

    def __init__(self) -> None:
        self._project_service = ProjectService()

    async def execute(
        self,
        offset: int,
        limit: int,
        order_by: str,
        reverse: bool,
    ) -> list[Project]:
        return await self._project_service.get_list(limit, offset, order_by, reverse)
