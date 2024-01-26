from typing import Annotated, Any

from fastapi import HTTPException, Query
from pydantic import UUID4

from src.dependencies import SQLASessionDep
from src.user.usermodels import UserDB
from src.user.userschemas import UserGet
from src.user.userservice import get_user_db


async def get_user_list_params(page: Annotated[int, Query(gt=0)] = 1,
                               limit: Annotated[int, Query(gt=0, le=10)] = 5,
                               ordering: Annotated[str, Query(enum=list(UserGet.model_fields))] = 'username',
                               reverse: bool = False) -> dict[str, Any]:
    offset = (page - 1) * limit
    return {'offset': offset,
            'limit': limit,
            'ordering': ordering,
            'reverse': reverse}


async def validate_user_id(session: SQLASessionDep,
                           user_id: UUID4) -> UserDB:
    user = await get_user_db(session=session, id=user_id)

    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    return user
