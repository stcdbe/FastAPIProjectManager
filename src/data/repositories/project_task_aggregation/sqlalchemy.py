from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import selectinload

from src.data.models.project_model import ProjectModel
from src.data.repositories.project_task_aggregation.base import AbstractProjectTaskAggregationRepository
from src.data.repositories.project_task_aggregation.converters import convert_project_task_aggregation_model_to_entity
from src.data.repositories.sqlalchemy_base import SQLAlchemyRepository
from src.domain.project.exc import ProjectNotFoundError
from src.domain.project_task_aggregation.entities import ProjectTaskAggregation


class SQLAlchemyProjectTaskAggregationRepository(AbstractProjectTaskAggregationRepository, SQLAlchemyRepository):
    async def get_one_project_with_tasks_by_guid(self, project_guid: UUID) -> ProjectTaskAggregation:
        stmt = select(ProjectModel).where(ProjectModel.guid == project_guid).options(selectinload(ProjectModel.tasks))
        try:
            async with self._get_session() as session:
                res = await session.execute(stmt)
                project_model = res.scalars().one()
                return convert_project_task_aggregation_model_to_entity(project_model)

        except NoResultFound as e:
            msg = f"Project {project_guid} not found"
            raise ProjectNotFoundError(msg) from e
