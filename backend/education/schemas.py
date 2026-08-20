"""education 기능의 API DTO."""

from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class EducationDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    school: str
    degree: str
    field_of_study: Optional[str]
    start_date: date
    end_date: Optional[date]


class EducationCreateRequest(BaseModel):
    school: str = Field(min_length=1, max_length=200)
    degree: str = Field(min_length=1, max_length=100)
    field_of_study: Optional[str] = Field(default=None, max_length=200)
    start_date: date
    end_date: Optional[date] = None


class EducationUpdateRequest(EducationCreateRequest):
    pass
