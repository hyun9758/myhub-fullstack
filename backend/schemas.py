"""기능 하나에 속하지 않는 공용 DTO."""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    database: str
    postgres_version: str
