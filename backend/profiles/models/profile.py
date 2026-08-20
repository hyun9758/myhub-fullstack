"""profile 엔티티 — 테이블의 모양. 이력서 소유자는 한 명뿐이라 CRUD 중 Read/Update만 있다."""

from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger, DateTime, Identity, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from db import Base


class Profile(Base):
    __tablename__ = "profile"

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    full_name: Mapped[str] = mapped_column(Text, nullable=False)
    headline: Mapped[str] = mapped_column(Text, nullable=False)
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
