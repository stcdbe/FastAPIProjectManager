from src.domain.task.entities import TaskCreateData, TaskPatchData
from src.presentation.task.schemas import TaskCreateScheme, TaskPatchScheme


def convert_task_create_scheme_to_entity(
    scheme: TaskCreateScheme,
) -> TaskCreateData:
    return TaskCreateData(
        title=scheme.title,
        description=scheme.description,
        is_completed=scheme.is_completed,
        executor_guid=scheme.executor_guid,
    )


def convert_task_patch_scheme_to_entity(
    scheme: TaskPatchScheme,
) -> TaskPatchData:
    return TaskPatchData(
        title=scheme.title,
        description=scheme.description,
        is_completed=scheme.is_completed,
        executor_guid=scheme.executor_guid,
    )
