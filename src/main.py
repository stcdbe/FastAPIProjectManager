from contextlib import asynccontextmanager
from typing import AsyncGenerator, Any

from fastapi import FastAPI
from fastapi.routing import APIRouter

from src.auth.authviews import login_router
from src.database.redis import init_redis
from src.user.userviews import user_router
from src.project.projectviews import project_router
from src.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Any, None]:
    await init_redis()
    yield


app = FastAPI(debug=settings.DEBUG,
              title='FastAPI Project Manager',
              version='0.1.3',
              lifespan=lifespan)

main_api_router = APIRouter()

main_api_router.include_router(login_router, prefix='/auth', tags=['Auth'])
main_api_router.include_router(user_router, prefix='/users', tags=['Users'])
main_api_router.include_router(project_router, prefix='/projects', tags=['Projects'])

app.include_router(main_api_router, prefix='/api')
