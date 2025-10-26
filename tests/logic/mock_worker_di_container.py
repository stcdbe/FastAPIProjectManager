from functools import lru_cache

from punq import Container


@lru_cache(maxsize=1)
def get_mock_worker_di_container() -> Container: ...
