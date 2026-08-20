"""profile 기능의 ORM 접근 계층. 실제 select/update 호출만 담당한다."""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from profiles.models.profile import Profile
from profiles.schemas import ProfileUpdateRequest


def get_profile(db: Session) -> Optional[Profile]:
    return db.scalars(select(Profile).order_by(Profile.id).limit(1)).first()


def update_profile(db: Session, entity: Profile, data: ProfileUpdateRequest) -> Profile:
    entity.full_name = data.full_name
    entity.headline = data.headline
    entity.summary = data.summary
    entity.photo = data.photo
    entity.badges = data.badges
    entity.birth = data.birth
    entity.address = data.address
    entity.military_service = data.military_service
    entity.email = data.email
    entity.mobile = data.mobile
    entity.affiliation = data.affiliation
    entity.social = [link.model_dump() for link in data.social]
    db.commit()
    db.refresh(entity)  # updated_at은 DB가 계산한 값이라 다시 읽어와야 한다.
    return entity
