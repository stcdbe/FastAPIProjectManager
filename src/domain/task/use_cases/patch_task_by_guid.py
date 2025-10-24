from uuid import UUID


class PatchTaskByGUIDUseCase:
    async def execute(self) -> UUID: ...
