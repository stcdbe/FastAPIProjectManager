from abc import ABC, abstractmethod
from typing import Any


class AbstractJWTManager(ABC):
    @abstractmethod
    def encode_token(self, payload: dict[str, Any]) -> str: ...

    @abstractmethod
    def decode_token(self, token: str) -> dict[str, Any]: ...
