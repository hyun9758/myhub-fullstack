"""profile 기능의 API DTO."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ProfileDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    full_name: str
    headline: str
    summary: Optional[str]
    updated_at: datetime


class ProfileResponse(BaseModel):
    profile: ProfileDTO


class ProfileUpdateRequest(BaseModel):
    full_name: str = Field(min_length=1, max_length=100)
    headline: str = Field(min_length=1, max_length=200)
    summary: Optional[str] = Field(default=None, max_length=2000)
