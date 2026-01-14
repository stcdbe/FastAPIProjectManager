from logging.config import dictConfig as loggingDictConfig

import uvicorn

from src.config import get_settings
from src.main import create_app

app = create_app()

if __name__ == "__main__":
    loggingDictConfig(get_settings().LOG_CONFIG)
    uvicorn.run(
        app="asgi:app",
        host=get_settings().HOST,
        port=get_settings().PORT,
        reload=get_settings().DEBUG,
    )
