from src.data.models.task.task_model import TaskModel
from src.domain.task.entities import Task


def convert_task_model_to_entity(
    model: TaskModel,
) -> Task:
    return Task(
        guid=model.guid,
        created_at=model.created_at,
        updated_at=model.updated_at,
        title=model.title,
        description=model.description,
        is_completed=model.is_completed,
        project_guid=model.project_guid,
        executor_guid=model.executor_guid,
    )
