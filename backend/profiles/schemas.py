"""profile 기능의 API DTO."""

from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class SocialLink(BaseModel):
    platform: str = Field(min_length=1, max_length=50)
    label: str = Field(min_length=1, max_length=100)
    url: str = Field(min_length=1, max_length=500)


class ProfileDTO(BaseModel):
    """방문자에게 내려가는 기본 모양. 민감 필드는 profiles/service.py에서 방문자일 때 None으로 가린다
    (PRD UR-13). 소유자 조회 시에는 실제 값이 채워져 내려간다 — 필드 자체는 동일하게 유지한다."""

    model_config = ConfigDict(from_attributes=True)

    full_name: str
    headline: str
    summary: Optional[str]
    photo: Optional[str]
    badges: List[str]
    birth: Optional[date]
    address: Optional[str]
    military_service: Optional[str]
    email: Optional[str]
    mobile: Optional[str]
    affiliation: Optional[str]
    social: List[SocialLink]
    updated_at: datetime


class ProfileResponse(BaseModel):
    profile: ProfileDTO


class ProfileUpdateRequest(BaseModel):
    full_name: str = Field(min_length=1, max_length=100)
    headline: str = Field(min_length=1, max_length=200)
    summary: Optional[str] = Field(default=None, max_length=2000)
    photo: Optional[str] = Field(default=None, max_length=1000)
    badges: List[str] = Field(default_factory=list)
    birth: Optional[date] = None
    address: Optional[str] = Field(default=None, max_length=200)
    military_service: Optional[str] = Field(default=None, max_length=100)
    email: Optional[str] = Field(default=None, max_length=200)
    mobile: Optional[str] = Field(default=None, max_length=50)
    affiliation: Optional[str] = Field(default=None, max_length=200)
    social: List[SocialLink] = Field(default_factory=list)
