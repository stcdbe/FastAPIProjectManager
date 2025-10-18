from pydantic import UUID4, BaseModel


class ErrorResponse(BaseModel):
    detail: str


class GUIDResponse(BaseModel):
    guid: UUID4
