"""auth 기능의 HTTP 엔드포인트. HTTP 관심사만 다루고 판단은 service.py에 위임한다."""

from typing import Optional

from fastapi import APIRouter, Cookie, Response

from auth import service
from auth.schemas import AuthStatus, LoginRequest

router = APIRouter(prefix="/api/auth/session", tags=["auth"])


@router.post("", response_model=AuthStatus)
def login(body: LoginRequest, response: Response):
    """관리자 비밀 코드를 검증하고, 통과하면 서명된 세션 쿠키를 발급한다."""
    return service.login(body, response)


@router.get("", response_model=AuthStatus)
def get_session(session: Optional[str] = Cookie(default=None)):
    """현재 브라우저가 유효한 관리자 세션 쿠키를 가지고 있는지 확인한다."""
    return service.get_session(session)


@router.delete("", response_model=AuthStatus)
def logout(response: Response):
    """세션 쿠키를 제거해 로그아웃 처리한다 (방문자 모드로 복귀)."""
    return service.logout(response)
