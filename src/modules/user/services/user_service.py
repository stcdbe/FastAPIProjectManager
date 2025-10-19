from datetime import UTC, datetime
from uuid import UUID, uuid4

from src.modules.user.data.repositories.sqlalchemy import SQLAlchemyUserRepository
from src.modules.user.entities.user import User, UserCreateData, UserPatchData
from src.modules.user.services.hasher_service import BcryptHasher


class UserService:
    def __init__(
        self,
    ) -> None:
        self._user_repository = SQLAlchemyUserRepository()
        self._hasher = BcryptHasher()

    async def get_list(
        self,
        offset: int,
        limit: int,
        order_by: str,
        reverse: bool,
    ) -> list[User]:
        return await self._user_repository.get_list(
            limit=limit,
            offset=offset,
            order_by=order_by,
            reverse=reverse,
        )

    async def get_one_by_guid(self, guid: UUID) -> User:
        user = await self._user_repository.get_one_by_guid(guid)

        if user.is_deleted:
            raise

        return user

    async def get_one_by_username(self, username: str) -> User:
        user = await self._user_repository.get_one_by_username(username)

        if user.is_deleted:
            raise

        return user

    async def create_one(self, user_create_data: UserCreateData) -> UUID:
        user = User(
            guid=uuid4(),
            username=user_create_data.username,
            email=user_create_data.email,
            password=self._hasher.get_psw_hash(user_create_data.password),
            first_name=user_create_data.first_name,
            second_name=user_create_data.second_name,
            gender=user_create_data.gender,
            company=user_create_data.company,
            join_date=user_create_data.join_date,
            job_title=user_create_data.job_title,
            date_of_birth=user_create_data.date_of_birth,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
            is_deleted=False,
            deleted_at=None,
        )
        user.password = self._hasher.get_psw_hash(user.password)
        return await self._user_repository.create_one(user=user)

    async def patch_one(self, user: User, user_patch_data: UserPatchData) -> UUID:
        if user_patch_data.username is not None:
            user.username = user_patch_data.username

        if user_patch_data.email is not None:
            user.email = user_patch_data.email

        if user_patch_data.password is not None:
            user.password = self._hasher.get_psw_hash(user.password)

        user.first_name = user_patch_data.first_name
        user.second_name = user_patch_data.second_name
        user.gender = user_patch_data.gender
        user.company = user_patch_data.company
        user.join_date = user_patch_data.join_date
        user.job_title = user_patch_data.job_title
        user.date_of_birth = user_patch_data.date_of_birth

        user.updated_at = datetime.now(UTC)
        return await self._user_repository.patch_one(user=user)

    async def soft_delete_one_by_guid(self, user: User) -> UUID:
        user.is_deleted = True
        user.deleted_at = datetime.now(UTC)
        return await self._user_repository.patch_one(user)
