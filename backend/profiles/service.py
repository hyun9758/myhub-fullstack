"""profile 기능의 업무 규칙. 데이터가 없으면 404로 변환한다."""

from fastapi import HTTPException
from sqlalchemy.orm import Session

from profiles import repository
from profiles.schemas import ProfileDTO, ProfileResponse, ProfileUpdateRequest


def get_profile(db: Session) -> ProfileResponse:
    entity = repository.get_profile(db)
    if entity is None:
        raise HTTPException(status_code=404, detail="프로필이 아직 없습니다.")
    return ProfileResponse(profile=ProfileDTO.model_validate(entity))


def update_profile(db: Session, payload: ProfileUpdateRequest) -> ProfileResponse:
    entity = repository.get_profile(db)
    if entity is None:
        raise HTTPException(status_code=404, detail="프로필이 아직 없습니다.")
    entity = repository.update_profile(db, entity, payload.full_name, payload.headline, payload.summary)
    return ProfileResponse(profile=ProfileDTO.model_validate(entity))
