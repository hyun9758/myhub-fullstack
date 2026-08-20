"""skills 기능의 API DTO."""

from typing import List

from pydantic import BaseModel, ConfigDict, Field


class LanguageProficiency(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    level: str = Field(min_length=1, max_length=50)


class SkillsDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    tech: List[str]
    languages: List[LanguageProficiency]


class SkillsUpdateRequest(BaseModel):
    tech: List[str] = Field(default_factory=list)
    languages: List[LanguageProficiency] = Field(default_factory=list)
