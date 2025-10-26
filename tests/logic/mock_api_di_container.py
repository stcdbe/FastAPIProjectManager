from functools import lru_cache

from punq import Container, Scope
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.config import get_settings
from src.data.repositories.project.base import AbstractProjectRepository
from src.data.repositories.project.sqlachemy import SQLAlchemyProjectRepository
from src.data.repositories.task.base import AbstractTaskRepository
from src.data.repositories.task.sqlalchemy import SQLAlchemyTaskRepository
from src.data.repositories.user.base import AbstractUserRepository
from src.data.repositories.user.sqlalchemy import SQLAlchemyUserRepository
from src.infra.worker.broker import RabbitMQMessageBroker
from src.logic.api_di_container import _get_api_di_container
from tests.infra.mock_broker import MockRabbitMQMessageBroker


@lru_cache(maxsize=1)
def get_mock_api_di_container() -> Container:
    container = _get_api_di_container()

    # sqlalchemy engine and sessionmaker
    test_async_engine = create_async_engine(
        url=get_settings().PG_URL_TEST.unicode_string(),
        echo=False,
        pool_pre_ping=True,
        pool_size=10,
        pool_recycle=3600,
    )
    test_async_session_factory = async_sessionmaker(
        bind=test_async_engine,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
    )
    # repos
    container.register(
        AbstractUserRepository,
        factory=lambda: SQLAlchemyUserRepository(test_async_session_factory),
        scope=Scope.singleton,
    )
    container.register(
        AbstractProjectRepository,
        factory=lambda: SQLAlchemyProjectRepository(test_async_session_factory),
        scope=Scope.singleton,
    )
    container.register(
        AbstractTaskRepository,
        factory=lambda: SQLAlchemyTaskRepository(test_async_session_factory),
        scope=Scope.singleton,
    )
    # infra
    container.register(
        RabbitMQMessageBroker,
        factory=MockRabbitMQMessageBroker,
        scope=Scope.singleton,
    )

    return container
