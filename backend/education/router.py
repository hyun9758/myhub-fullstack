"""education 기능의 HTTP 엔드포인트. 목록 조회만 로그인 없이도 공개(이력서는 누구나 볼 수 있어야 함)."""

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth.service import require_auth
from db import get_db
from education import service
from education.schemas import EducationCreateRequest, EducationDTO, EducationUpdateRequest

router = APIRouter(prefix="/api/educations", tags=["education"])


@router.get("", response_model=List[EducationDTO])
def list_educations(db: Session = Depends(get_db)):
    return service.list_educations(db)


@router.post("", response_model=EducationDTO, status_code=201)
def create_education(
    payload: EducationCreateRequest,
    db: Session = Depends(get_db),
    _: None = Depends(require_auth),
):
    return service.create_education(db, payload)


@router.put("/{education_id}", response_model=EducationDTO)
def update_education(
    education_id: int,
    payload: EducationUpdateRequest,
    db: Session = Depends(get_db),
    _: None = Depends(require_auth),
):
    return service.update_education(db, education_id, payload)


@router.delete("/{education_id}", status_code=204)
def delete_education(
    education_id: int,
    db: Session = Depends(get_db),
    _: None = Depends(require_auth),
):
    service.delete_education(db, education_id)
