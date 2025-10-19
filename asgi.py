from logging.config import dictConfig

import uvicorn

from src.config import get_settings
from src.main import create_app

app = create_app()

if __name__ == "__main__":
    dictConfig(get_settings().LOG_CONFIG)
    uvicorn.run(
        app="asgi:app",
        host=get_settings().HOST,
        port=get_settings().PORT,
        reload=get_settings().DEBUG,
        log_config=get_settings().LOG_CONFIG,
    )
