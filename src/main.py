from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.routing import APIRouter

from src.config import get_settings

# from src.modules.project.views.routes import project_v1_router
from src.modules.user.views.user.routes import user_v1_router


def get_api_v1_router() -> APIRouter:
    api_v1_router = APIRouter(prefix="/api/v1")

    for router in (
        user_v1_router,
        # project_v1_router,
    ):
        api_v1_router.include_router(router=router)

    return api_v1_router


# def get_api_v2_router() -> APIRouter: ...
# def get_api_v3_router() -> APIRouter: ...


def create_app() -> FastAPI:
    app = FastAPI(
        debug=get_settings().DEBUG,
        title="FastAPI Project Manager",
        version="0.3.0",
        docs_url=get_settings().DOCS_URL,
        redoc_url=get_settings().REDOC_URL,
        default_response_class=ORJSONResponse,
    )

    for router in (get_api_v1_router(),):
        app.include_router(router)

    return app
