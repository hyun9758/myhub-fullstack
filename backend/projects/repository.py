"""project 기능의 ORM 접근 계층."""

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from projects.models.project import Project
from projects.schemas import ProjectCreateRequest, ProjectUpdateRequest


def list_projects(db: Session) -> List[Project]:
    # year 최신순 정렬(DRQ-018). 같은 연도 내 순서는 id(등록 순)로 안정 정렬된다 (OPEN-03 참고).
    return list(db.scalars(select(Project).order_by(Project.year.desc(), Project.id.desc())).all())


def get_project(db: Session, project_id: int) -> Optional[Project]:
    return db.get(Project, project_id)


def create_project(db: Session, data: ProjectCreateRequest) -> Project:
    entity = Project(
        category=data.category,
        year=data.year,
        period=data.period,
        name=data.name,
        role=data.role,
        description=data.description,
        links=[link.model_dump() for link in data.links],
    )
    db.add(entity)
    db.commit()
    db.refresh(entity)
    return entity


def update_project(db: Session, entity: Project, data: ProjectUpdateRequest) -> Project:
    entity.category = data.category
    entity.year = data.year
    entity.period = data.period
    entity.name = data.name
    entity.role = data.role
    entity.description = data.description
    entity.links = [link.model_dump() for link in data.links]
    db.commit()
    db.refresh(entity)
    return entity


def delete_project(db: Session, entity: Project) -> None:
    db.delete(entity)
    db.commit()
