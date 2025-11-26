from dataclasses import dataclass


@dataclass(eq=False, frozen=True, slots=True)
class BaseAppError(Exception):
    msg: str

    def __str__(self) -> str:
        return self.msg

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.msg}"
