from logging.config import dictConfig as loggingDictConfig

from src.config import get_settings
from src.main import create_app

loggingDictConfig(get_settings().LOG_CONFIG)
app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app="asgi:app",
        host=get_settings().HOST,
        port=get_settings().PORT,
        reload=get_settings().DEBUG,
    )
