"""profile 기능의 ORM 접근 계층. 실제 select/update 호출만 담당한다."""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from profiles.models.profile import Profile


def get_profile(db: Session) -> Optional[Profile]:
    return db.scalars(select(Profile).order_by(Profile.id).limit(1)).first()


def update_profile(db: Session, entity: Profile, full_name: str, headline: str, summary: Optional[str]) -> Profile:
    entity.full_name = full_name
    entity.headline = headline
    entity.summary = summary
    db.commit()
    db.refresh(entity)  # updated_at은 DB가 계산한 값이라 다시 읽어와야 한다.
    return entity
