"""profile 엔티티 — 테이블의 모양. 이력서 소유자는 한 명뿐이라 CRUD 중 Read/Update만 있다."""

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Integer, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from db import Base


class Profile(Base):
    __tablename__ = "profile"

    # 명시적 Identity() 대신 표준 autoincrement 기본키를 쓴다 — Postgres에선 SERIAL로 동작하고,
    # SQLite(테스트용)에서도 rowid 별칭으로 그대로 호환된다.
    # (SQLite는 선언 타입이 정확히 'INTEGER'일 때만 자동증가 별칭이 붙으므로 BigInteger 대신 Integer 사용)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(Text, nullable=False)
    headline: Mapped[str] = mapped_column(Text, nullable=False)
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
