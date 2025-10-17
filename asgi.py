from logging.config import dictConfig

import uvicorn

from src.config import settings

if __name__ == "__main__":
    dictConfig(settings.LOG_CONFIG)
    uvicorn.run(
        app="asgi:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
