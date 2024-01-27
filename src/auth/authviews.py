from datetime import timedelta
from typing import Annotated

from fastapi import Depends, APIRouter

from src.auth.authdependencies import validate_oauth2_form
from src.config import settings
from src.auth.authschemas import Token
from src.user.usermodels import UserDB
from src.auth.authutils import generate_token


login_router = APIRouter()


@login_router.post('/create_token',
                   status_code=201,
                   response_model=Token,
                   name='Create an access token')
async def create_token(user: Annotated[UserDB, Depends(validate_oauth2_form)]) -> dict[str, str]:
    token = await generate_token(user_id=str(user.id),
                                 expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES))
    return {'access_token': token, 'token_type': 'bearer'}
