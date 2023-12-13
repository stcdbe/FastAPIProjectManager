import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_some_users(client: AsyncClient) -> None:
    params = {'offset': 0,
              'limit': 5,
              'ordering': 'username',
              'reverse': False}
    res = await client.get('/api/users', params=params)
    assert res.status_code == 200


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient) -> None:
    user_data = {'username': 'test_username',
                 'email': 'test_email@example.com',
                 'password': 'passwordpassword'}
    res = await client.post('/api/users', json=user_data)
    created_user = res.json()
    assert res.status_code == 201
    assert created_user
    assert created_user.get('password') is None
    assert created_user['username'] == user_data['username']
    assert created_user['email'] == user_data['email']
    assert created_user['join_date']
    assert created_user['id']


@pytest.mark.asyncio
async def test_get_me(client: AsyncClient, user_token_headers: dict[str, str]) -> None:
    res = await client.get('/api/users/me', headers=user_token_headers)
    current_user = res.json()
    assert res.status_code == 200
    assert current_user


@pytest.mark.asyncio
async def test_patch_me(client: AsyncClient, user_token_headers: dict[str, str]) -> None:
    patch_user_data = {'username': 'test_patch_username',
                       'email': 'test_patch_user@example.com',
                       'password': 'passwordpassword',
                       'company': 'company',
                       'job_title': 'job_title',
                       'fullname': 'fullname',
                       'age': 20,
                       'sex': 'M'}
    res = await client.patch('/api/users/me',
                             json=patch_user_data,
                             headers=user_token_headers)
    upd_user = res.json()
    assert res.status_code == 200
    assert upd_user
    assert upd_user.get('password') is None
    patch_user_data.pop('password')
    for key, val in patch_user_data.items():
        assert upd_user[key] == val


@pytest.mark.asyncio
async def test_get_user(client: AsyncClient, test_user_uuid: str) -> None:
    res = await client.get(f'/api/users/{test_user_uuid}')
    user = res.json()
    assert res.status_code == 200
    assert user['id'] == test_user_uuid
