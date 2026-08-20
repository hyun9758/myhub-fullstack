"""project 엔티티 — 목록형(0개 이상). links는 개별 항목이 고유 ID를 갖지 않는 통째 저장 값이라
JSON 컬럼에 배열째로 둔다 (profile.social과 동일 패턴, DRQ-019)."""

from typing import Any, Dict, List, Optional

from sqlalchemy import Integer, JSON, Text
from sqlalchemy.orm import Mapped, mapped_column

from db import Base


class Project(Base):
    __tablename__ = "project"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category: Mapped[str] = mapped_column(Text, nullable=False)
    year: Mapped[str] = mapped_column(Text, nullable=False)
    period: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    role: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    links: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, nullable=False, default=list)
