"""career 기능의 API DTO."""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class CareerDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    institution: str
    period: str
    role: str
    description: Optional[str]


class CareerCreateRequest(BaseModel):
    institution: str = Field(min_length=1, max_length=200)
    period: str = Field(min_length=1, max_length=100)
    role: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)


class CareerUpdateRequest(CareerCreateRequest):
    pass
