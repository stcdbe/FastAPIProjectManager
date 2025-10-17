from multiprocessing import cpu_count

from src.config import get_settings

bind = f"{get_settings().HOST}:{get_settings().PORT}"
workers = (cpu_count() * 2) + 1
worker_class = "uvicorn.workers.UvicornWorker"
capture_output = True
loglevel = "warning"
