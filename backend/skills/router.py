"""skills 기능의 HTTP 엔드포인트."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth.service import require_auth
from db import get_db
from skills import service
from skills.schemas import SkillsDTO, SkillsUpdateRequest

router = APIRouter(prefix="/api/skills", tags=["skills"])


@router.get("", response_model=SkillsDTO)
def get_skills(db: Session = Depends(get_db)):
    return service.get_skills(db)


@router.put("", response_model=SkillsDTO)
def update_skills(
    payload: SkillsUpdateRequest,
    db: Session = Depends(get_db),
    _: None = Depends(require_auth),
):
    return service.update_skills(db, payload)
