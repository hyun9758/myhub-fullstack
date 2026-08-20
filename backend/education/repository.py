"""education 기능의 ORM 접근 계층."""

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from education.models.education import Education
from education.schemas import EducationCreateRequest, EducationUpdateRequest


def list_educations(db: Session) -> List[Education]:
    # 최신 학력이 먼저 보이도록 정렬한다.
    return list(db.scalars(select(Education).order_by(Education.start_date.desc())).all())


def get_education(db: Session, education_id: int) -> Optional[Education]:
    return db.get(Education, education_id)


def create_education(db: Session, data: EducationCreateRequest) -> Education:
    entity = Education(
        school=data.school,
        degree=data.degree,
        field_of_study=data.field_of_study,
        start_date=data.start_date,
        end_date=data.end_date,
    )
    db.add(entity)
    db.commit()
    db.refresh(entity)
    return entity


def update_education(db: Session, entity: Education, data: EducationUpdateRequest) -> Education:
    entity.school = data.school
    entity.degree = data.degree
    entity.field_of_study = data.field_of_study
    entity.start_date = data.start_date
    entity.end_date = data.end_date
    db.commit()
    db.refresh(entity)
    return entity


def delete_education(db: Session, entity: Education) -> None:
    db.delete(entity)
    db.commit()
