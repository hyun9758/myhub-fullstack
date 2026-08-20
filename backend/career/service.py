"""career 기능의 업무 규칙. 없는 id에 대한 수정/삭제는 404로 변환한다."""

from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from career import repository
from career.schemas import CareerCreateRequest, CareerDTO, CareerUpdateRequest


def list_careers(db: Session) -> List[CareerDTO]:
    entities = repository.list_careers(db)
    return [CareerDTO.model_validate(e) for e in entities]


def create_career(db: Session, payload: CareerCreateRequest) -> CareerDTO:
    entity = repository.create_career(db, payload)
    return CareerDTO.model_validate(entity)


def update_career(db: Session, career_id: int, payload: CareerUpdateRequest) -> CareerDTO:
    entity = repository.get_career(db, career_id)
    if entity is None:
        raise HTTPException(status_code=404, detail="해당 경력 항목이 없습니다.")
    entity = repository.update_career(db, entity, payload)
    return CareerDTO.model_validate(entity)


def delete_career(db: Session, career_id: int) -> None:
    entity = repository.get_career(db, career_id)
    if entity is None:
        raise HTTPException(status_code=404, detail="해당 경력 항목이 없습니다.")
    repository.delete_career(db, entity)
