"""education 기능의 업무 규칙. 없는 id에 대한 수정/삭제는 404로 변환한다."""

from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from education import repository
from education.schemas import EducationCreateRequest, EducationDTO, EducationUpdateRequest


def list_educations(db: Session) -> List[EducationDTO]:
    entities = repository.list_educations(db)
    return [EducationDTO.model_validate(e) for e in entities]


def create_education(db: Session, payload: EducationCreateRequest) -> EducationDTO:
    entity = repository.create_education(db, payload)
    return EducationDTO.model_validate(entity)


def update_education(db: Session, education_id: int, payload: EducationUpdateRequest) -> EducationDTO:
    entity = repository.get_education(db, education_id)
    if entity is None:
        raise HTTPException(status_code=404, detail="해당 학력 항목이 없습니다.")
    entity = repository.update_education(db, entity, payload)
    return EducationDTO.model_validate(entity)


def delete_education(db: Session, education_id: int) -> None:
    entity = repository.get_education(db, education_id)
    if entity is None:
        raise HTTPException(status_code=404, detail="해당 학력 항목이 없습니다.")
    repository.delete_education(db, entity)
