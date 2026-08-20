"""education 엔티티 — 여러 건을 넣고 뺄 수 있는 목록형 리소스라 CRUD 전체가 필요하다."""

from datetime import date
from typing import Optional

from sqlalchemy import Date, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from db import Base


class Education(Base):
    __tablename__ = "education"

    # 명시적 Identity() 대신 표준 autoincrement 기본키를 쓴다 — Postgres에선 SERIAL로 동작하고,
    # SQLite(테스트용)에서도 rowid 별칭으로 그대로 호환된다.
    # (SQLite는 선언 타입이 정확히 'INTEGER'일 때만 자동증가 별칭이 붙으므로 BigInteger 대신 Integer 사용)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    school: Mapped[str] = mapped_column(Text, nullable=False)
    degree: Mapped[str] = mapped_column(Text, nullable=False)
    field_of_study: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    gpa: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
