from functools import lru_cache

from punq import Container, Scope

from src.config import get_settings
from src.data.repositories.project.base import AbstractProjectRepository
from src.data.repositories.project.sqlachemy import SQLAlchemyProjectRepository
from src.data.repositories.task.base import AbstractTaskRepository
from src.data.repositories.task.sqlalchemy import SQLAlchemyTaskRepository
from src.data.repositories.user.base import AbstractUserRepository
from src.data.repositories.user.cache_redis import RedisUserCasheRepository
from src.data.repositories.user.cashe_base import AbstractUserCacheRepository
from src.data.repositories.user.sqlalchemy import SQLAlchemyUserRepository
from src.domain.project.use_cases.create_project import CreateProjectUseCase
from src.domain.project.use_cases.delete_project_by_guid import DeleteProjectByGUIDUseCase
from src.domain.project.use_cases.get_project_by_guid_by_guid import GetProjectByGUIDUseCase
from src.domain.project.use_cases.get_project_list import GetProjectListUseCase
from src.domain.project.use_cases.patch_project_by_guid import PatchProjectByGUIDUseCase
from src.domain.project_task_aggregation.use_cases.send_project_report import SendProjectReportUseCase
from src.domain.task.use_cases.create_task import CreateTaskUseCase
from src.domain.task.use_cases.delete_task_by_guid import DeleteTaskByGUIDUseCase
from src.domain.task.use_cases.get_list import GetTaskListByProjectGUIDUseCase
from src.domain.task.use_cases.patch_task_by_guid import PatchTaskByGUIDUseCase
from src.domain.user.use_cases.authenticate_user_by_token import AuthenticateUserByTokenUseCase
from src.domain.user.use_cases.create_user import CreateUserUseCase
from src.domain.user.use_cases.delete_user_by_guid import DeleteUserByGUIDUseCase
from src.domain.user.use_cases.generate_user_token import GenerateUserTokenUseCase
from src.domain.user.use_cases.get_one_user_by_guid import GetOneUserByGUIDUseCase
from src.domain.user.use_cases.get_user_list import GetUserListUseCase
from src.domain.user.use_cases.patch_user_by_guid import PatchUserByGUIDUseCase
from src.domain.user.use_cases.refresh_user_token import RefreshUserTokenUseCase
from src.infra.brokers.base import AbstractMessageBroker
from src.infra.brokers.rabbitmq.broker import RabbitMQMessageBroker
from src.services.auth_service import AuthService
from src.services.hasher_service import HasherService
from src.services.project_service import ProjectService
from src.services.task_service import TaskService
from src.services.user_service import UserService


def _get_api_di_container() -> Container:
    container = Container()
    # repos
    container.register(
        AbstractUserRepository,
        factory=lambda: SQLAlchemyUserRepository(get_settings().PG_URL.unicode_string()),
        scope=Scope.singleton,
    )
    container.register(
        AbstractUserCacheRepository,
        factory=lambda: RedisUserCasheRepository(get_settings().REDIS_URL.unicode_string()),
        scope=Scope.singleton,
    )
    container.register(
        AbstractProjectRepository,
        factory=lambda: SQLAlchemyProjectRepository(get_settings().PG_URL.unicode_string()),
        scope=Scope.singleton,
    )
    container.register(
        AbstractTaskRepository,
        factory=lambda: SQLAlchemyTaskRepository(get_settings().PG_URL.unicode_string()),
        scope=Scope.singleton,
    )
    # infra
    container.register(
        AbstractMessageBroker,
        factory=lambda: RabbitMQMessageBroker(get_settings().RMQ_URL.unicode_string()),
        scope=Scope.singleton,
    )
    # services
    container.register(AuthService)
    container.register(HasherService)
    container.register(UserService)
    container.register(ProjectService)
    container.register(TaskService)
    # user use cases
    container.register(AuthenticateUserByTokenUseCase)
    container.register(GenerateUserTokenUseCase)
    container.register(RefreshUserTokenUseCase)
    container.register(GetUserListUseCase)
    container.register(CreateUserUseCase)
    container.register(GetOneUserByGUIDUseCase)
    container.register(PatchUserByGUIDUseCase)
    container.register(DeleteUserByGUIDUseCase)
    # project use cases
    container.register(GetProjectListUseCase)
    container.register(CreateProjectUseCase)
    container.register(GetProjectByGUIDUseCase)
    container.register(PatchProjectByGUIDUseCase)
    container.register(DeleteProjectByGUIDUseCase)
    # task use cases
    container.register(GetTaskListByProjectGUIDUseCase)
    container.register(CreateTaskUseCase)
    container.register(PatchTaskByGUIDUseCase)
    container.register(DeleteTaskByGUIDUseCase)
    # project task aggregation use cases
    container.register(SendProjectReportUseCase)

    return container


@lru_cache(maxsize=1)
def get_api_di_container() -> Container:
    return _get_api_di_container()
