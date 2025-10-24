from uuid import UUID

from src.domain.project.entities.project import ProjectCreateData, ProjectPatchData, ProjectReportSendData
from src.presentation.project.schemas import ProjectCreateScheme, ProjectPatchScheme, ProjectReportSendDataScheme


def convert_project_create_scheme_to_entity(
    scheme: ProjectCreateScheme,
) -> ProjectCreateData:
    return ProjectCreateData(
        title=scheme.title,
        description=scheme.description,
        tech_stack=tuple(scheme.tech_stack),
        additional_metadata=scheme.additional_metadata,
        start_date=scheme.start_date,
        constraint_date=scheme.constraint_date,
        mentor_guid=scheme.mentor_guid,
    )


def convert_project_patch_scheme_to_entity(
    scheme: ProjectPatchScheme,
) -> ProjectPatchData:
    if scheme.tech_stack is None:
        tech_stack = None
    else:
        tech_stack = tuple(scheme.tech_stack)

    return ProjectPatchData(
        title=scheme.title,
        description=scheme.description,
        tech_stack=tech_stack,
        additional_metadata=scheme.additional_metadata,
        start_date=scheme.start_date,
        constraint_date=scheme.constraint_date,
        mentor_guid=scheme.mentor_guid,
    )


def convert_project_report_send_data_scheme_to_entity(
    scheme: ProjectReportSendDataScheme,
) -> ProjectReportSendData:
    return ProjectReportSendData(
        project_guid=scheme.project_guid,
        email=scheme.email,
    )
