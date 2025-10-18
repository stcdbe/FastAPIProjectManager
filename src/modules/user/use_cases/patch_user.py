from uuid import UUID


class PatchUserUseCase:
    async def execute(self) -> UUID: ...
