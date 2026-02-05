from functools import lru_cache

from punq import Container, Scope

from src.config import get_settings
from src.data.repositories.project.base import AbstractProjectRepository
from src.data.repositories.project.sqlachemy import SQLAlchemyProjectRepository
from src.data.repositories.task.base import AbstractTaskRepository
from src.data.repositories.task.sqlalchemy import SQLAlchemyTaskRepository
from src.data.repositories.user.base import AbstractUserRepository
from src.data.repositories.user.sqlalchemy import SQLAlchemyUserRepository
from src.infra.brokers.base import AbstractMessageBroker
from src.infra.brokers.console.broker import ConsoleMessageBroker
from src.logic.api_di_container import _get_api_di_container


@lru_cache(maxsize=1)
def get_mock_api_di_container() -> Container:
    container = _get_api_di_container()
    # repos
    container.register(
        AbstractUserRepository,
        factory=lambda: SQLAlchemyUserRepository(get_settings().PG_URL_TEST.unicode_string()),
        scope=Scope.singleton,
    )
    container.register(
        AbstractProjectRepository,
        factory=lambda: SQLAlchemyProjectRepository(get_settings().PG_URL_TEST.unicode_string()),
        scope=Scope.singleton,
    )
    container.register(
        AbstractTaskRepository,
        factory=lambda: SQLAlchemyTaskRepository(get_settings().PG_URL_TEST.unicode_string()),
        scope=Scope.singleton,
    )
    # infra
    container.register(
        AbstractMessageBroker,
        factory=ConsoleMessageBroker,
        scope=Scope.singleton,
    )

    return container
