"""education 엔티티 — 여러 건을 넣고 뺄 수 있는 목록형 리소스라 CRUD 전체가 필요하다."""

from datetime import date
from typing import Optional

from sqlalchemy import BigInteger, Date, Identity, Text
from sqlalchemy.orm import Mapped, mapped_column

from db import Base


class Education(Base):
    __tablename__ = "education"

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    school: Mapped[str] = mapped_column(Text, nullable=False)
    degree: Mapped[str] = mapped_column(Text, nullable=False)
    field_of_study: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
