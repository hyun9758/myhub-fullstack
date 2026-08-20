"""MyHub backend — Step 1: FastAPI <-> Supabase(PostgreSQL) connectivity check.

이 파일은 Step 1의 목표(파이썬 서버가 Supabase DB와 실제로 통신하는지 확인)만 담당한다.
접속 정보는 .env 에서 로드하며, URL 파싱 문제를 피하기 위해 항목별(host/port/dbname/user/password)로
psycopg.connect()에 전달한다 (비밀번호에 특수문자가 있어도 안전).
"""

import os
from typing import Optional

import psycopg
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

load_dotenv()

app = FastAPI(title="MyHub Backend")


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
    """이력서 소유자의 기본 프로필 정보 응답 DTO."""

    id: int
    full_name: str
    headline: str
    summary: Optional[str]
    updated_at: str


@app.get("/profile", response_model=dict[str, Profile])
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
        return {
            "profile": Profile(
                id=row[0],
                full_name=row[1],
                headline=row[2],
                summary=row[3],
                updated_at=row[4].isoformat(),
            )
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"DB 조회 실패: {e}")
