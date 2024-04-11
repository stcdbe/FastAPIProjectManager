from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.routing import APIRouter

from src.auth.auth_views import login_router
from src.config import settings
from src.database.redis import init_redis
from src.project.project_views import project_router
from src.user.user_views import user_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    await init_redis()
    yield


app = FastAPI(debug=settings.DEBUG,
              title='FastAPI Project Manager',
              version='0.1.8',
              lifespan=lifespan,
              docs_url=settings.DOCS_URL,
              redoc_url=settings.REDOC_URL)

main_api_router = APIRouter(prefix='/api')

for router in (login_router, user_router, project_router):
    main_api_router.include_router(router=router)

app.include_router(main_api_router)
