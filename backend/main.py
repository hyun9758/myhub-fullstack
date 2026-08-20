"""MyHub backend — 엔드포인트 정의. Step 5부터 SQL은 main.py에 직접 쓰지 않는다
(health의 select version() 은 엔티티로 표현할 대상이 아니므로 예외)."""

import os
from contextlib import asynccontextmanager
from typing import Optional

from dotenv import load_dotenv
from fastapi import Cookie, Depends, FastAPI, HTTPException, Response
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from sqlalchemy import select, text
from sqlalchemy.orm import Session

import models
import schemas
from db import engine, get_db
from init_db import init_database

load_dotenv()

SESSION_COOKIE_NAME = "session"
SESSION_MAX_AGE_SECONDS = 60 * 60 * 24 * 7  # 7일


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 엔티티 기준으로 테이블이 있는지 확인하고, 없으면 만든다. 비어 있으면 초기 데이터 1건을 넣는다.
    init_database()
    yield
    engine.dispose()


app = FastAPI(title="MyHub Backend", lifespan=lifespan)


def get_serializer() -> URLSafeTimedSerializer:
    return URLSafeTimedSerializer(os.environ["SESSION_SECRET"], salt="myhub-auth")


def require_auth(session: Optional[str] = Cookie(default=None)) -> None:
    """관리자 전용 엔드포인트 가드. 서명된 세션 쿠키가 없거나 유효하지 않으면 401."""
    if session is None:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다.")
    try:
        get_serializer().loads(session, max_age=SESSION_MAX_AGE_SECONDS)
    except (BadSignature, SignatureExpired):
        raise HTTPException(status_code=401, detail="세션이 만료되었거나 유효하지 않습니다.")


def load_profile(db: Session) -> models.Profile:
    profile = db.scalars(select(models.Profile).order_by(models.Profile.id).limit(1)).first()
    if profile is None:
        raise HTTPException(status_code=404, detail="프로필이 아직 없습니다.")
    return profile


@app.get("/health", response_model=schemas.HealthResponse)
def health(db: Session = Depends(get_db)):
    """Supabase(PostgreSQL) 연결 상태와 버전 정보를 반환한다. (raw SQL — 엔티티로 표현할 대상이 아님)"""
    try:
        version = db.scalar(text("select version()"))
        return schemas.HealthResponse(database="연결됨", postgres_version=version)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"DB 연결 실패: {e}")


@app.get("/api/profile", response_model=schemas.ProfileResponse)
def get_profile(db: Session = Depends(get_db)):
    """`profile` 엔티티에서 이름·한 줄 소개·상세 소개·마지막 수정 시각을 조회한다."""
    entity = load_profile(db)
    return schemas.ProfileResponse(profile=schemas.Profile.model_validate(entity))


@app.put("/api/profile", response_model=schemas.ProfileResponse)
def update_profile(
    body: schemas.ProfileUpdate,
    db: Session = Depends(get_db),
    _: None = Depends(require_auth),
):
    """로그인(관리자)한 경우에만 프로필을 수정한다. updated_at은 엔티티 정의(onupdate)로 자동 갱신된다."""
    entity = load_profile(db)

    entity.full_name = body.full_name
    entity.headline = body.headline
    entity.summary = body.summary

    db.commit()
    db.refresh(entity)  # updated_at은 DB가 계산한 값이라 다시 읽어와야 한다.

    return schemas.ProfileResponse(profile=schemas.Profile.model_validate(entity))


@app.post("/api/auth/session", response_model=schemas.AuthStatus)
def login(body: schemas.LoginRequest, response: Response):
    """관리자 비밀 코드를 검증하고, 통과하면 서명된 세션 쿠키를 발급한다."""
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
    return schemas.AuthStatus(authenticated=True)


@app.get("/api/auth/session", response_model=schemas.AuthStatus)
def get_session(session: Optional[str] = Cookie(default=None)):
    """현재 브라우저가 유효한 관리자 세션 쿠키를 가지고 있는지 확인한다."""
    if session is None:
        return schemas.AuthStatus(authenticated=False)
    try:
        get_serializer().loads(session, max_age=SESSION_MAX_AGE_SECONDS)
    except (BadSignature, SignatureExpired):
        return schemas.AuthStatus(authenticated=False)
    return schemas.AuthStatus(authenticated=True)


@app.delete("/api/auth/session", response_model=schemas.AuthStatus)
def logout(response: Response):
    """세션 쿠키를 제거해 로그아웃 처리한다 (방문자 모드로 복귀)."""
    response.delete_cookie(key=SESSION_COOKIE_NAME)
    return schemas.AuthStatus(authenticated=False)
