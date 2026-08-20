"""career 엔티티 — 여러 건을 넣고 뺄 수 있는 목록형 리소스. period는 구조화된 날짜가 아니라
자유 텍스트 한 줄로 저장한다 (ADR-0003, PRD 원 스키마)."""

from typing import Optional

from sqlalchemy import Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from db import Base


class Career(Base):
    __tablename__ = "career"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    institution: Mapped[str] = mapped_column(Text, nullable=False)
    period: Mapped[str] = mapped_column(Text, nullable=False)
    role: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
