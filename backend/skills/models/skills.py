"""skills 엔티티 — 단일형(1개). tech/languages는 개별 항목이 고유 ID를 갖지 않고
저장 시 항상 전체를 통째로 교체하는 값이라, JSON 컬럼 하나에 배열째로 저장한다 (그릴링 합의)."""

from typing import Any, Dict, List

from sqlalchemy import Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column

from db import Base


class Skills(Base):
    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tech: Mapped[List[str]] = mapped_column(JSON, nullable=False, default=list)
    languages: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, nullable=False, default=list)
