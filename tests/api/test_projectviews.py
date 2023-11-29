import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_some_projects(client: AsyncClient) -> None:
    params = {'offset': 0,
              'limit': 5,
              'ordering': 'created_at',
              'reverse': False}
    res = await client.get('/api/projects', params=params)
    assert res.status_code == 200


@pytest.mark.asyncio
async def test_create_project(client: AsyncClient, user_token_headers: dict[str, str]) -> None:
    test_project_data = {"project_title": "test_title",
                         "project_description": "test_description",
                         "tech_stack": ["string"],
                         "start_date": "2050-01-01T00:00:00",
                         "constraint_date": "2051-01-01T00:00:00",
                         "mentor_id": None}
    res = await client.post('/api/projects',
                            json=test_project_data,
                            headers=user_token_headers)
    created_project = res.json()
    assert res.status_code == 201
    assert created_project
    assert created_project['id']
    assert created_project['created_at']
    for key, val in test_project_data.items():
        assert created_project[key] == val


@pytest.mark.asyncio
async def test_get_project(client: AsyncClient, test_project_uuid: str) -> None:
    res = await client.get(f'/api/projects/{test_project_uuid}')
    project = res.json()
    assert res.status_code == 200
    assert project
    assert project['id'] == test_project_uuid


@pytest.mark.asyncio
@pytest.mark.asyncio
async def test_patch_project(client: AsyncClient,
                             test_user_uuid: str,
                             test_project_uuid: str,
                             user_token_headers: dict[str, str]) -> None:
    test_patch_project_data = {"project_title": "test_patch_title",
                               "project_description": "test_patch_description",
                               "tech_stack": ["patch_string"],
                               "start_date": "2051-01-01T00:00:00",
                               "constraint_date": "2054-01-01T00:00:00",
                               "mentor_id": test_user_uuid}
    res = await client.patch(f'/api/projects/{test_project_uuid}',
                             json=test_patch_project_data,
                             headers=user_token_headers)
    upd_project = res.json()
    assert res.status_code == 200
    assert upd_project
    for key, val in test_patch_project_data.items():
        assert upd_project[key] == val


@pytest.mark.asyncio
async def test_create_project_task(client: AsyncClient,
                                   test_user_uuid: str,
                                   test_project_uuid: str,
                                   user_token_headers: dict[str, str]) -> None:
    test_task_data = {"task_title": "test_title",
                      "task_description": "test_description",
                      "is_completed": False,
                      "executor_id": test_user_uuid}
    res = await client.post(f'/api/projects/{test_project_uuid}',
                            json=test_task_data,
                            headers=user_token_headers)
    project_with_new_task = res.json()
    assert res.status_code == 201
    assert project_with_new_task
    assert test_task_data['task_title'] in [task['task_title'] for task in project_with_new_task['tasks']]
    assert test_task_data['task_description'] in [task['task_description'] for task in project_with_new_task['tasks']]
    assert test_task_data['executor_id'] in [task['executor_id'] for task in project_with_new_task['tasks']]


@pytest.mark.asyncio
async def test_patch_project_task(client: AsyncClient,
                                  test_project_uuid: str,
                                  test_task_uuid: str,
                                  user_token_headers: dict[str, str]) -> None:
    test_patch_task_data = {"task_title": "test_patch_title",
                            "task_description": "test_patch_description",
                            "is_completed": True,
                            "executor_id": None}
    res = await client.patch(f'/api/projects/{test_project_uuid}/tasks/{test_task_uuid}',
                             json=test_patch_task_data,
                             headers=user_token_headers)
    project_with_upd_task = res.json()
    assert res.status_code == 200
    assert project_with_upd_task
    assert test_patch_task_data['task_title'] in [task['task_title'] for task in project_with_upd_task['tasks']]
    assert test_patch_task_data['task_description'] in [task['task_description'] for task in project_with_upd_task['tasks']]


@pytest.mark.asyncio
async def test_del_project_task(client: AsyncClient,
                                test_project_uuid: str,
                                test_task_uuid: str,
                                user_token_headers: dict[str, str]) -> None:
    res = await client.delete(f'/api/projects/{test_project_uuid}/tasks/{test_task_uuid}',
                              headers=user_token_headers)
    assert res.status_code == 204


@pytest.mark.asyncio
async def test_del_project(client: AsyncClient,
                           test_project_uuid: str,
                           user_token_headers: dict[str, str]) -> None:
    res = await client.delete(f'/api/projects/{test_project_uuid}', headers=user_token_headers)
    assert res.status_code == 204
