"""project 기능의 API DTO."""

from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class ProjectLink(BaseModel):
    label: str = Field(min_length=1, max_length=50)
    # DRQ-019: URL 형식 검증(DRQ-014와 동일 규칙 재사용). http(s):// 로 시작해야 저장을 통과한다.
    url: str = Field(min_length=1, max_length=500, pattern=r"^https?://")


class ProjectDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    category: str
    year: str
    period: Optional[str]
    name: str
    role: str
    description: Optional[str]
    links: List[ProjectLink]


class ProjectCreateRequest(BaseModel):
    category: str = Field(min_length=1, max_length=50)
    year: str = Field(min_length=4, max_length=10)
    period: Optional[str] = Field(default=None, max_length=100)
    name: str = Field(min_length=1, max_length=200)
    role: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    links: List[ProjectLink] = Field(default_factory=list)


class ProjectUpdateRequest(ProjectCreateRequest):
    pass
