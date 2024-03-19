from contextlib import asynccontextmanager
from typing import AsyncGenerator, Any

from fastapi import FastAPI
from fastapi.routing import APIRouter

from src.auth.auth_views import login_router
from src.database.redis import init_redis
from src.user.user_views import user_router
from src.project.project_views import project_router
from src.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Any, None]:
    await init_redis()
    yield


app = FastAPI(debug=settings.DEBUG,
              title='FastAPI Project Manager',
              version='0.1.7',
              lifespan=lifespan,
              docs_url=settings.DOCS_URL,
              redoc_url=settings.REDOC_URL)

main_api_router = APIRouter(prefix='/api')

main_api_router.include_router(login_router)
main_api_router.include_router(user_router)
main_api_router.include_router(project_router)

app.include_router(main_api_router)
