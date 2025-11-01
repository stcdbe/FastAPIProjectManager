from datetime import UTC, datetime
from logging import getLogger
from uuid import UUID, uuid4

from src.data.repositories.user.base import AbstractUserRepository
from src.data.repositories.user.cashe_base import AbstractUserCacheRepository
from src.domain.user.entities import User, UserCreateData, UserPatchData
from src.domain.user.exc import UserIsSoftDeletedError
from src.services.hasher_service import HasherService

logger = getLogger()


class UserService:
    __slots__ = (
        "_hasher_service",
        "_user_cache_repository",
        "_user_repository",
    )

    def __init__(
        self,
        user_cache_repository: AbstractUserCacheRepository,
        user_repository: AbstractUserRepository,
        hasher_service: HasherService,
    ) -> None:
        self._user_cache_repository = user_cache_repository
        self._user_repository = user_repository
        self._hasher_service = hasher_service

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
        user_from_cashe = await self._user_cache_repository.get_one(guid)

        if user_from_cashe is None:
            user = await self._user_repository.get_one_by_guid(guid)
        else:
            user = user_from_cashe

        if user.is_deleted:
            logger.warning("Attempt to fetch soft deleted user by guid %s", guid)
            msg = f"User {guid} not found"
            raise UserIsSoftDeletedError(msg)

        if user_from_cashe is None:
            await self._user_cache_repository.add_one(user)

        return user

    async def get_one_by_username(self, username: str) -> User:
        user = await self._user_repository.get_one_by_username(username)

        if user.is_deleted:
            logger.warning("Attempt to fetch soft deleted user by username %s", username)
            msg = f"User {username} not found"
            raise UserIsSoftDeletedError(msg)

        return user

    async def create_one(self, user_create_data: UserCreateData) -> UUID:
        user = User(
            guid=uuid4(),
            username=user_create_data.username,
            email=user_create_data.email,
            password=self._hasher_service.get_psw_hash(user_create_data.password),
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
        user_guid = await self._user_repository.create_one(user=user)

        await self._user_cache_repository.delete_one(user_guid)

        return user_guid

    async def patch_one(self, user: User, user_patch_data: UserPatchData) -> UUID:
        if user_patch_data.username is not None:
            user.username = user_patch_data.username

        if user_patch_data.email is not None:
            user.email = user_patch_data.email

        if user_patch_data.password is not None:
            user.password = self._hasher_service.get_psw_hash(user.password)

        user.first_name = user_patch_data.first_name
        user.second_name = user_patch_data.second_name
        user.gender = user_patch_data.gender
        user.company = user_patch_data.company
        user.join_date = user_patch_data.join_date
        user.job_title = user_patch_data.job_title
        user.date_of_birth = user_patch_data.date_of_birth
        user.updated_at = datetime.now(UTC)

        user_guid = await self._user_repository.patch_one(user=user)

        await self._user_cache_repository.delete_one(user_guid)

        return user_guid

    async def soft_delete_one_by_guid(self, user: User) -> UUID:
        user.is_deleted = True
        user.deleted_at = datetime.now(UTC)

        user_guid = await self._user_repository.patch_one(user)
        await self._user_cache_repository.delete_one(user_guid)

        return user_guid
