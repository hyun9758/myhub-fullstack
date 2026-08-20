"""profile 기능의 업무 규칙. 데이터가 없으면 404로 변환한다."""

from fastapi import HTTPException
from sqlalchemy.orm import Session

from profiles import repository
from profiles.schemas import ProfileDTO, ProfileResponse, ProfileUpdateRequest

# 방문자에게는 노출하지 않는 민감 필드 (PRD UR-13, 요구사항 그릴링 6.2 합의).
SENSITIVE_FIELDS = ("birth", "address", "military_service")


def get_profile(db: Session, authenticated: bool) -> ProfileResponse:
    entity = repository.get_profile(db)
    if entity is None:
        raise HTTPException(status_code=404, detail="프로필이 아직 없습니다.")
    dto = ProfileDTO.model_validate(entity)
    if not authenticated:
        dto = dto.model_copy(update={field: None for field in SENSITIVE_FIELDS})
    return ProfileResponse(profile=dto)


def update_profile(db: Session, payload: ProfileUpdateRequest) -> ProfileResponse:
    entity = repository.get_profile(db)
    if entity is None:
        raise HTTPException(status_code=404, detail="프로필이 아직 없습니다.")
    entity = repository.update_profile(db, entity, payload)
    # 수정은 항상 소유자만 가능하므로(require_auth), 민감 필드를 포함해 전체를 그대로 반환한다.
    return ProfileResponse(profile=ProfileDTO.model_validate(entity))
