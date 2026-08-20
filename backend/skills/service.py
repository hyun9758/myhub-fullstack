"""skills 기능의 업무 규칙. 데이터가 없으면 404로 변환한다."""

from fastapi import HTTPException
from sqlalchemy.orm import Session

from skills import repository
from skills.schemas import SkillsDTO, SkillsUpdateRequest


def get_skills(db: Session) -> SkillsDTO:
    entity = repository.get_skills(db)
    if entity is None:
        raise HTTPException(status_code=404, detail="스킬 정보가 아직 없습니다.")
    return SkillsDTO.model_validate(entity)


def update_skills(db: Session, payload: SkillsUpdateRequest) -> SkillsDTO:
    entity = repository.get_skills(db)
    if entity is None:
        raise HTTPException(status_code=404, detail="스킬 정보가 아직 없습니다.")
    entity = repository.update_skills(
        db,
        entity,
        payload.tech,
        [lang.model_dump() for lang in payload.languages],
    )
    return SkillsDTO.model_validate(entity)
