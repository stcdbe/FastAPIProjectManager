from src.data.models.project_model import ProjectModel
from src.data.repositories.project.converters import convert_project_model_to_entity
from src.data.repositories.task.converters import convert_task_model_to_entity
from src.domain.project_task_aggregation.entities import ProjectTaskAggregation


def convert_project_task_aggregation_model_to_entity(
    model: ProjectModel,
) -> ProjectTaskAggregation:
    return ProjectTaskAggregation(
        project=convert_project_model_to_entity(model),
        tasks=[convert_task_model_to_entity(task_model) for task_model in model.tasks],
    )
