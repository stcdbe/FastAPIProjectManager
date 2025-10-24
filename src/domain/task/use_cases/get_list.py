from src.domain.task.entities.task import Task


class GetTaskListUseCase:
    async def execute(self) -> list[Task]: ...
