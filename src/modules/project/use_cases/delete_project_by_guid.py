from uuid import UUID


class DeleteProjectByGUIDUseCase:
    async def execute(self, guid: UUID) -> UUID: ...
