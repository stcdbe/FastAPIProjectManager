from fastapi import FastAPI
from fastapi.routing import APIRouter

from src.config import settings
from src.modules.auth.views.routes import auth_router
from src.modules.project.views.routes import project_router
from src.modules.user.views.routes import user_router

app = FastAPI(
    debug=settings.DEBUG,
    title="FastAPI Project Manager",
    version="0.2.1",
    docs_url=settings.DOCS_URL,
    redoc_url=settings.REDOC_URL,
)

api_v1_router = APIRouter(prefix="/api/v1")

for router in (auth_router, user_router, project_router):
    api_v1_router.include_router(router=router)

app.include_router(router=api_v1_router)
