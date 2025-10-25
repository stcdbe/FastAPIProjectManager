from dataclasses import dataclass

from src.domain.project.entities import Project
from src.domain.task.entities import Task


@dataclass(slots=True)
class ProjectTaskAggregation:
    project: Project
    tasks: list[Task]
