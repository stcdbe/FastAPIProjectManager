from datetime import UTC, datetime, timedelta
from secrets import token_urlsafe
from typing import Final
from uuid import UUID, uuid4

from src.domain.project.entities import Project
from src.domain.task.entities import Task
from src.domain.user.entities import User
from src.services.hasher_service import HasherService

MOCK_USER_AUTH_GUID: Final[UUID] = uuid4()
MOCK_USER_GET_GUID: Final[UUID] = uuid4()
MOCK_USER_PATCH_GUID: Final[UUID] = uuid4()
MOCK_USER_DELETE_GUID: Final[UUID] = uuid4()

MOCK_PROJECT_GET_GUID: Final[UUID] = uuid4()
MOCK_PROJECT_PATCH_GUID: Final[UUID] = uuid4()
MOCK_PROJECT_DELETE_GUID: Final[UUID] = uuid4()

MOCK_TASK_GET_GUID: Final[UUID] = uuid4()
MOCK_TASK_PATCH_GUID: Final[UUID] = uuid4()
MOCK_TASK_DELETE_GUID: Final[UUID] = uuid4()

_mock_users_fields = (
    (MOCK_USER_AUTH_GUID, "auth_username", "auth@email.com"),
    (MOCK_USER_GET_GUID, "get_username", "get@email.com"),
    (MOCK_USER_PATCH_GUID, "patch_username", "patch@email.com"),
    (MOCK_USER_DELETE_GUID, "delete_username", "delete@email.com"),
)
_mock_projets_fields = (
    (MOCK_PROJECT_GET_GUID, "get_title"),
    (MOCK_PROJECT_PATCH_GUID, "patch_title"),
    (MOCK_PROJECT_DELETE_GUID, "delete_title"),
)
_mock_tasks_fields = (
    (MOCK_TASK_GET_GUID, "get_title"),
    (MOCK_TASK_PATCH_GUID, "patch_title"),
    (MOCK_TASK_DELETE_GUID, "delete_title"),
)

mock_user_entities = tuple(
    User(
        guid=guid,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
        username=username,
        email=email,
        password=HasherService().get_psw_hash("passwordpassword"),
        first_name=None,
        second_name=None,
        gender=None,
        company=None,
        join_date=None,
        job_title=None,
        date_of_birth=None,
        is_deleted=False,
        deleted_at=None,
    )
    for guid, username, email in _mock_users_fields
)
mock_project_entities = tuple(
    Project(
        guid=guid,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
        title=title,
        description=token_urlsafe(16),
        tech_stack=(token_urlsafe(16), token_urlsafe(16)),
        additional_metadata={"meta": "data"},
        start_date=datetime.now(UTC).date() + timedelta(days=1),
        constraint_date=datetime.now(UTC).date() + timedelta(days=10),
        creator_guid=MOCK_USER_AUTH_GUID,
        mentor_guid=None,
    )
    for guid, title in _mock_projets_fields
)
mock_task_entities = tuple(
    Task(
        guid=guid,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
        title=title,
        description=token_urlsafe(16),
        is_completed=False,
        project_guid=MOCK_PROJECT_GET_GUID,
        executor_guid=MOCK_USER_AUTH_GUID,
    )
    for guid, title in _mock_tasks_fields
)
