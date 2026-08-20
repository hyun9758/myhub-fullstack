"""MyHub backend — Step 1: FastAPI <-> Supabase(PostgreSQL) connectivity check.

이 파일은 Step 1의 목표(파이썬 서버가 Supabase DB와 실제로 통신하는지 확인)만 담당한다.
접속 정보는 .env 에서 로드하며, URL 파싱 문제를 피하기 위해 항목별(host/port/dbname/user/password)로
psycopg.connect()에 전달한다 (비밀번호에 특수문자가 있어도 안전).
"""

import os

import psycopg
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

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
