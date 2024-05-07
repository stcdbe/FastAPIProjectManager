from multiprocessing import cpu_count

from src.config import settings

bind = "0.0.0.0:" + str(settings.PORT)
workers = (cpu_count() * 2) + 1
worker_class = "uvicorn.workers.UvicornWorker"
capture_output = True
loglevel = "warning"
