from datetime import UTC, datetime
from uuid import UUID, uuid4

from src.data.repositories.project.sqlachemy import SQLAlchemyProjectRepository
from src.domain.project.entities.project import Project, ProjectCreateData, ProjectPatchData


class ProjectService:
    __slots__ = ("_project_repository",)

    def __init__(self) -> None:
        self._project_repository = SQLAlchemyProjectRepository()

    async def get_list(
        self,
        limit: int,
        offset: int,
        order_by: str,
        reverse: bool,
    ) -> list[Project]:
        return await self._project_repository.get_list(
            limit=limit,
            offset=offset,
            order_by=order_by,
            reverse=reverse,
        )

    async def get_one_by_guid(self, guid: UUID) -> Project:
        return await self._project_repository.get_one_by_guid(guid=guid)

    async def create_one(self, creator_guid: UUID, project_create_data: ProjectCreateData) -> UUID:
        project = Project(
            guid=uuid4(),
            title=project_create_data.title,
            description=project_create_data.title,
            tech_stack=project_create_data.tech_stack,
            additional_metadata=project_create_data.additional_metadata,
            start_date=project_create_data.start_date,
            constraint_date=project_create_data.constraint_date,
            creator_guid=creator_guid,
            mentor_guid=project_create_data.mentor_guid,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )
        return await self._project_repository.create_one(project=project)

    async def patch_one(self, project: Project, project_patch_data: ProjectPatchData) -> UUID:
        if project_patch_data.title is not None:
            project.title = project_patch_data.title

        if project_patch_data.description is not None:
            project.description = project_patch_data.description

        if project_patch_data.tech_stack is not None:
            project.tech_stack = project_patch_data.tech_stack

        if project_patch_data.additional_metadata is not None:
            project.additional_metadata = project_patch_data.additional_metadata

        if project_patch_data.start_date is not None:
            project.start_date = project_patch_data.start_date

        if project_patch_data.constraint_date is not None:
            project.constraint_date = project_patch_data.constraint_date

        project.mentor_guid = project_patch_data.mentor_guid
        project.updated_at = datetime.now(UTC)

        return await self._project_repository.patch_one(project=project)

    async def delete_one(self, project: Project) -> UUID:
        return await self._project_repository.delete_one(project=project)
