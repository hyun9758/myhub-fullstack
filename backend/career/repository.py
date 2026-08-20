"""career 기능의 ORM 접근 계층."""

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from career.models.career import Career
from career.schemas import CareerCreateRequest, CareerUpdateRequest


def list_careers(db: Session) -> List[Career]:
    # period가 자유 텍스트라 사전식 정렬이다 — 항상 정확한 날짜순은 아닐 수 있다 (DRQ-011, OPEN-02).
    return list(db.scalars(select(Career).order_by(Career.period.desc())).all())


def get_career(db: Session, career_id: int) -> Optional[Career]:
    return db.get(Career, career_id)


def create_career(db: Session, data: CareerCreateRequest) -> Career:
    entity = Career(
        institution=data.institution,
        period=data.period,
        role=data.role,
        description=data.description,
    )
    db.add(entity)
    db.commit()
    db.refresh(entity)
    return entity


def update_career(db: Session, entity: Career, data: CareerUpdateRequest) -> Career:
    entity.institution = data.institution
    entity.period = data.period
    entity.role = data.role
    entity.description = data.description
    db.commit()
    db.refresh(entity)
    return entity


def delete_career(db: Session, entity: Career) -> None:
    db.delete(entity)
    db.commit()
