from src.data.models.project_model import ProjectModel
from src.domain.project.entities import Project


def convert_project_model_to_entity(model: ProjectModel) -> Project:
    return Project(
        guid=model.guid,
        title=model.title,
        description=model.description,
        tech_stack=model.tech_stack,
        additional_metadata=model.additional_metadata,
        start_date=model.start_date,
        constraint_date=model.constraint_date,
        creator_guid=model.creator_guid,
        mentor_guid=model.mentor_guid,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )
