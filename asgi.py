import uvicorn

from src.main import app
from src.config import settings


if __name__ == '__main__':
    uvicorn.run('asgi:src', host='0.0.0.0', port=settings.PORT)
