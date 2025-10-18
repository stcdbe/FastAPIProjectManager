from uuid import UUID


class CreateUserUseCase:
    async def execute(self) -> UUID: ...
