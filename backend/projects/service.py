"""project 기능의 업무 규칙. 없는 id에 대한 수정/삭제는 404로 변환한다."""

from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from projects import repository
from projects.schemas import ProjectCreateRequest, ProjectDTO, ProjectUpdateRequest


def list_projects(db: Session) -> List[ProjectDTO]:
    entities = repository.list_projects(db)
    return [ProjectDTO.model_validate(e) for e in entities]


def create_project(db: Session, payload: ProjectCreateRequest) -> ProjectDTO:
    entity = repository.create_project(db, payload)
    return ProjectDTO.model_validate(entity)


def update_project(db: Session, project_id: int, payload: ProjectUpdateRequest) -> ProjectDTO:
    entity = repository.get_project(db, project_id)
    if entity is None:
        raise HTTPException(status_code=404, detail="해당 프로젝트 항목이 없습니다.")
    entity = repository.update_project(db, entity, payload)
    return ProjectDTO.model_validate(entity)


def delete_project(db: Session, project_id: int) -> None:
    entity = repository.get_project(db, project_id)
    if entity is None:
        raise HTTPException(status_code=404, detail="해당 프로젝트 항목이 없습니다.")
    repository.delete_project(db, entity)
