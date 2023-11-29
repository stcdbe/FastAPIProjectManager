from asyncio import get_event_loop_policy, AbstractEventLoop
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.config import settings
from src.database.dbmodels import BaseModelDB
from src.database.db import get_session
from src.database.redis import init_redis
from src.main import app


PGURLTEST = (f'postgresql+asyncpg://{settings.PGUSERTEST}:{settings.PGPASSWORDTEST}@'
             f'{settings.PGHOSTTEST}:{settings.PGPORTTEST}/{settings.PGDBTEST}')


test_async_engine = create_async_engine(url=PGURLTEST,
                                        echo=False,
                                        pool_pre_ping=True,
                                        pool_size=10,
                                        pool_recycle=3600)

test_async_session = async_sessionmaker(bind=test_async_engine,
                                        expire_on_commit=False,
                                        class_=AsyncSession)


async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
    async with test_async_session() as test_session:
        yield test_session


app.dependency_overrides[get_session] = override_get_session


@pytest_asyncio.fixture(autouse=True, scope='session')
async def prepare_db() -> None:
    await init_redis()
    async with test_async_engine.begin() as conn:
        await conn.run_sync(BaseModelDB.metadata.drop_all)
        await conn.run_sync(BaseModelDB.metadata.create_all)
    yield
    async with test_async_engine.begin() as conn:
        await conn.run_sync(BaseModelDB.metadata.drop_all)


@pytest.fixture(scope='session')
def event_loop() -> AbstractEventLoop:
    loop = get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session')
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://test') as cli:
        yield cli


@pytest_asyncio.fixture(scope='session')
async def user_token_headers(client: AsyncClient) -> dict[str, str]:
    user_data = {'username': 'auth_username',
                 'email': 'auth_email@example.com',
                 'password': 'passwordpassword'}
    await client.post('/api/users', json=user_data)

    auth_form_data = {'username': user_data['username'], 'password': user_data['password']}
    res = await client.post('/api/auth/create_token', data=auth_form_data)

    access_token = res.json()['access_token']
    return {'Authorization': f'Bearer {access_token}'}


@pytest_asyncio.fixture(scope='session')
async def test_user_uuid(client: AsyncClient, user_token_headers: dict[str, str]) -> str:
    res = await client.get('/api/users/me', headers=user_token_headers)
    return res.json()['id']


@pytest_asyncio.fixture(scope='session')
async def test_project_uuid(client: AsyncClient, user_token_headers: dict[str, str]) -> str:
    project_data = {'project_title': 'project_title',
                    'project_description': 'project_description',
                    'tech_stack': ['string1'],
                    'start_date': '2050-01-01T00:00:00.000Z',
                    'constraint_date': '2051-01-01T00:00:00.000Z',
                    'mentor_id': None}
    res = await client.post('/api/projects',
                            json=project_data,
                            headers=user_token_headers)
    return res.json()['id']


@pytest_asyncio.fixture(scope='session')
async def test_task_uuid(client: AsyncClient,
                         user_token_headers: dict[str, str],
                         test_user_uuid: str,
                         test_project_uuid: str) -> str:
    task_data = {'task_title': 'task_title',
                 'task_description': 'task_description',
                 'is_completed': False,
                 'executor_id': test_user_uuid}

    res = await client.post(f'/api/projects/{test_project_uuid}',
                            json=task_data,
                            headers=user_token_headers)
    project = res.json()
    project_tasks = project['tasks']
    return project_tasks[0]['id']
