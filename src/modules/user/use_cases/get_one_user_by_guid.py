from uuid import UUID

from src.modules.user.entities.user import User


class GetOneUserByGUIDUseCase:
    def execute(self, guid: UUID) -> User: ...
