"""profile 기능의 HTTP 엔드포인트."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth.service import optional_auth, require_auth
from db import get_db
from profiles import service
from profiles.schemas import ProfileResponse, ProfileUpdateRequest

router = APIRouter(prefix="/api/profile", tags=["profiles"])


@router.get("", response_model=ProfileResponse)
def get_profile(db: Session = Depends(get_db), authenticated: bool = Depends(optional_auth)):
    return service.get_profile(db, authenticated)


@router.put("", response_model=ProfileResponse)
def update_profile(
    payload: ProfileUpdateRequest,
    db: Session = Depends(get_db),
    _: None = Depends(require_auth),
):
    return service.update_profile(db, payload)
