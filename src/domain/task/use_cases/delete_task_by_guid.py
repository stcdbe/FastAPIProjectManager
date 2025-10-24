from uuid import UUID


class DeleteTaskByGUIDUseCase:
    async def execute(self) -> UUID: ...
