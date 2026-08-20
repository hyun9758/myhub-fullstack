"""career 기능의 HTTP 엔드포인트. 목록 조회만 로그인 없이도 공개(이력서는 누구나 볼 수 있어야 함)."""

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth.service import require_auth
from db import get_db
from career import service
from career.schemas import CareerCreateRequest, CareerDTO, CareerUpdateRequest

router = APIRouter(prefix="/api/careers", tags=["career"])


@router.get("", response_model=List[CareerDTO])
def list_careers(db: Session = Depends(get_db)):
    return service.list_careers(db)


@router.post("", response_model=CareerDTO, status_code=201)
def create_career(
    payload: CareerCreateRequest,
    db: Session = Depends(get_db),
    _: None = Depends(require_auth),
):
    return service.create_career(db, payload)


@router.put("/{career_id}", response_model=CareerDTO)
def update_career(
    career_id: int,
    payload: CareerUpdateRequest,
    db: Session = Depends(get_db),
    _: None = Depends(require_auth),
):
    return service.update_career(db, career_id, payload)


@router.delete("/{career_id}", status_code=204)
def delete_career(
    career_id: int,
    db: Session = Depends(get_db),
    _: None = Depends(require_auth),
):
    service.delete_career(db, career_id)
