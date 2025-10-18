from uuid import UUID


class DeleteUserUseCase:
    async def execute(self) -> UUID: ...
