from uuid import UUID


class PatchProjectByGUIDUseCase:
    async def execute(self, guid: UUID) -> UUID: ...
