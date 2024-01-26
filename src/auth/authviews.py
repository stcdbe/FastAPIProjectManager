from datetime import timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from src.config import settings
from src.auth.authschemas import Token
from src.dependencies import SQLASessionDep
from src.user.userservice import get_user_db
from src.auth.authutils import generate_token, Hasher


login_router = APIRouter()


@login_router.post('/create_token',
                   status_code=201,
                   response_model=Token,
                   name='Create an access token')
async def create_token(session: SQLASessionDep,
                       form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> dict[str, str]:
    user = await get_user_db(session=session, username=form_data.username)

    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    if not Hasher.verify_psw(psw_to_check=form_data.password, hashed_psw=user.password):
        raise HTTPException(status_code=409, detail='Incorrect username or password')

    token = await generate_token(user_id=str(user.id),
                                 expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES))
    return {'access_token': token, 'token_type': 'bearer'}
