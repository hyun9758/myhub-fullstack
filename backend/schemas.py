"""Pydantic DTO — API의 모양. DB 엔티티 원형을 그대로 노출하지 않는다."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class Profile(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    full_name: str
    headline: str
    summary: Optional[str]
    updated_at: datetime


class ProfileResponse(BaseModel):
    profile: Profile


class ProfileUpdate(BaseModel):
    full_name: str = Field(min_length=1, max_length=100)
    headline: str = Field(min_length=1, max_length=200)
    summary: Optional[str] = Field(default=None, max_length=2000)


class LoginRequest(BaseModel):
    passcode: str


class AuthStatus(BaseModel):
    authenticated: bool


class HealthResponse(BaseModel):
    database: str
    postgres_version: str
