from src.modules.project.entities.project import Project


class GetProjectListUseCase:
    async def execute(
        self,
        offset: int,
        limit: int,
        order_by: str,
        reverse: bool,
    ) -> list[Project]: ...
