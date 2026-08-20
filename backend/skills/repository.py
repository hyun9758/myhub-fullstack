"""skills 기능의 ORM 접근 계층. profile과 동일하게 단일 레코드를 조회·수정만 한다."""

from typing import Any, Dict, List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from skills.models.skills import Skills


def get_skills(db: Session) -> Optional[Skills]:
    return db.scalars(select(Skills).order_by(Skills.id).limit(1)).first()


def update_skills(db: Session, entity: Skills, tech: List[str], languages: List[Dict[str, Any]]) -> Skills:
    entity.tech = tech
    entity.languages = languages
    db.commit()
    db.refresh(entity)
    return entity
