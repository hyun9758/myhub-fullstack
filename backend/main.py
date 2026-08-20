"""MyHub backend — Step 1: FastAPI <-> Supabase(PostgreSQL) connectivity check.

이 파일은 Step 1의 목표(파이썬 서버가 Supabase DB와 실제로 통신하는지 확인)만 담당한다.
접속 정보는 .env 에서 로드하며, URL 파싱 문제를 피하기 위해 항목별(host/port/dbname/user/password)로
psycopg.connect()에 전달한다 (비밀번호에 특수문자가 있어도 안전).
"""

import os
from typing import Optional

import psycopg
from dotenv import load_dotenv
from fastapi import Cookie, Depends, FastAPI, HTTPException, Response
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from pydantic import BaseModel

load_dotenv()

app = FastAPI(title="MyHub Backend")

SESSION_COOKIE_NAME = "session"
SESSION_MAX_AGE_SECONDS = 60 * 60 * 24 * 7  # 7일


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


def get_conn_info() -> dict:
    return {
        "host": os.environ["DB_HOST"],
        "port": os.environ["DB_PORT"],
        "dbname": os.environ["DB_NAME"],
        "user": os.environ["DB_USER"],
        "password": os.environ["DB_PASSWORD"],
    }


@app.get("/health")
def health():
    """Supabase(PostgreSQL) 연결 상태와 버전 정보를 JSON으로 반환한다.

    - 성공 시: {"database": "연결됨", "postgres_version": "..."}
    - 실패 시: 502와 함께 에러 메시지 반환 (.env 접속 정보를 확인할 것)
    """
    try:
        with psycopg.connect(**get_conn_info()) as conn:
            with conn.cursor() as cur:
                cur.execute("select version();")
                (version,) = cur.fetchone()
        return {"database": "연결됨", "postgres_version": version}
    except KeyError as e:
        raise HTTPException(status_code=500, detail=f".env 에 {e} 항목이 없습니다.")
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"DB 연결 실패: {e}")


class Profile(BaseModel):
    """이력서 소유자의 기본 프로필 정보 DTO. DB 테이블 원형을 그대로 노출하지 않고
    외부로 나가는 필드만 명시적으로 정의한다 (내부 전용 컬럼이 추가되어도 자동 유출되지 않음)."""

    id: int
    full_name: str
    headline: str
    summary: Optional[str]
    updated_at: str


class ProfileResponse(BaseModel):
    profile: Profile


@app.get("/api/profile", response_model=ProfileResponse)
def get_profile():
    """`public.profile` 테이블에서 이름·한 줄 소개·상세 소개·마지막 수정 시각을 조회한다.

    - 200: {"profile": {...}}
    - 404: 아직 데이터가 한 줄도 없는 경우 (테이블은 있으나 seed가 안 된 상태)
    """
    try:
        with psycopg.connect(**get_conn_info()) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    select id, full_name, headline, summary, updated_at
                    from public.profile
                    order by id
                    limit 1;
                    """
                )
                row = cur.fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="프로필이 아직 없습니다.")
        return ProfileResponse(
            profile=Profile(
                id=row[0],
                full_name=row[1],
                headline=row[2],
                summary=row[3],
                updated_at=row[4].isoformat(),
            )
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"DB 조회 실패: {e}")


class LoginRequest(BaseModel):
    passcode: str


class AuthStatus(BaseModel):
    authenticated: bool


@app.post("/api/auth/session", response_model=AuthStatus)
def login(body: LoginRequest, response: Response):
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
    return AuthStatus(authenticated=True)


@app.get("/api/auth/session", response_model=AuthStatus)
def get_session(session: Optional[str] = Cookie(default=None)):
    """현재 브라우저가 유효한 관리자 세션 쿠키를 가지고 있는지 확인한다."""
    if session is None:
        return AuthStatus(authenticated=False)
    try:
        get_serializer().loads(session, max_age=SESSION_MAX_AGE_SECONDS)
    except (BadSignature, SignatureExpired):
        return AuthStatus(authenticated=False)
    return AuthStatus(authenticated=True)


@app.delete("/api/auth/session", response_model=AuthStatus)
def logout(response: Response):
    """세션 쿠키를 제거해 로그아웃 처리한다 (방문자 모드로 복귀)."""
    response.delete_cookie(key=SESSION_COOKIE_NAME)
    return AuthStatus(authenticated=False)


class ProfileUpdate(BaseModel):
    full_name: str
    headline: str
    summary: Optional[str] = None


@app.put("/api/profile", response_model=ProfileResponse)
def update_profile(body: ProfileUpdate, _: None = Depends(require_auth)):
    """로그인(관리자)한 경우에만 프로필을 수정한다. id·updated_at은 서버가 자동 관리한다."""
    try:
        with psycopg.connect(**get_conn_info()) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    update public.profile
                    set full_name = %s, headline = %s, summary = %s, updated_at = now()
                    where id = (select id from public.profile order by id limit 1)
                    returning id, full_name, headline, summary, updated_at;
                    """,
                    (body.full_name, body.headline, body.summary),
                )
                row = cur.fetchone()
            conn.commit()
        if row is None:
            raise HTTPException(status_code=404, detail="수정할 프로필이 없습니다.")
        return ProfileResponse(
            profile=Profile(
                id=row[0],
                full_name=row[1],
                headline=row[2],
                summary=row[3],
                updated_at=row[4].isoformat(),
            )
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"DB 수정 실패: {e}")
