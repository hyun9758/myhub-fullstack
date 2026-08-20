"""project 기능의 HTTP 엔드포인트. 목록 조회만 로그인 없이도 공개(이력서는 누구나 볼 수 있어야 함)."""

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth.service import require_auth
from db import get_db
from projects import service
from projects.schemas import ProjectCreateRequest, ProjectDTO, ProjectUpdateRequest

router = APIRouter(prefix="/api/projects", tags=["projects"])


@router.get("", response_model=List[ProjectDTO])
def list_projects(db: Session = Depends(get_db)):
    return service.list_projects(db)


@router.post("", response_model=ProjectDTO, status_code=201)
def create_project(
    payload: ProjectCreateRequest,
    db: Session = Depends(get_db),
    _: None = Depends(require_auth),
):
    return service.create_project(db, payload)


@router.put("/{project_id}", response_model=ProjectDTO)
def update_project(
    project_id: int,
    payload: ProjectUpdateRequest,
    db: Session = Depends(get_db),
    _: None = Depends(require_auth),
):
    return service.update_project(db, project_id, payload)


@router.delete("/{project_id}", status_code=204)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    _: None = Depends(require_auth),
):
    service.delete_project(db, project_id)
