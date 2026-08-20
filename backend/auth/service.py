"""auth 기능의 업무 규칙. DB를 쓰지 않는 가장 얕은 패키지 — 비밀번호는 .env, 세션은 서명 쿠키."""

import os
from typing import Optional

from fastapi import Cookie, HTTPException, Response
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

from auth.schemas import AuthStatus, LoginRequest

SESSION_COOKIE_NAME = "session"
SESSION_MAX_AGE_SECONDS = 60 * 60 * 24 * 7  # 7일


def get_serializer() -> URLSafeTimedSerializer:
    return URLSafeTimedSerializer(os.environ["SESSION_SECRET"], salt="myhub-auth")


def require_auth(session: Optional[str] = Cookie(default=None)) -> None:
    """관리자 전용 엔드포인트 가드. 다른 기능(profiles, education)의 쓰기 요청이 이 의존성을 그대로 가져다 쓴다."""
    if session is None:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다.")
    try:
        get_serializer().loads(session, max_age=SESSION_MAX_AGE_SECONDS)
    except (BadSignature, SignatureExpired):
        raise HTTPException(status_code=401, detail="세션이 만료되었거나 유효하지 않습니다.")


def login(body: LoginRequest, response: Response) -> AuthStatus:
    if body.passcode != os.environ["ADMIN_PASSCODE"]:
        raise HTTPException(status_code=401, detail="비밀 코드가 올바르지 않습니다.")
    token = get_serializer().dumps({"owner": True})
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=token,
        max_age=SESSION_MAX_AGE_SECONDS,
        httponly=True,
        samesite="lax",
    )
    return AuthStatus(authenticated=True)


def get_session(session: Optional[str]) -> AuthStatus:
    if session is None:
        return AuthStatus(authenticated=False)
    try:
        get_serializer().loads(session, max_age=SESSION_MAX_AGE_SECONDS)
    except (BadSignature, SignatureExpired):
        return AuthStatus(authenticated=False)
    return AuthStatus(authenticated=True)


def logout(response: Response) -> AuthStatus:
    response.delete_cookie(key=SESSION_COOKIE_NAME)
    return AuthStatus(authenticated=False)
