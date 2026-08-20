"""SQLAlchemy 엔진 · 세션 · Base. 접속 정보는 항목별로 전달해 URL 파싱 특수문자 문제를 피한다."""

import os
from typing import Iterator

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

load_dotenv()

DATABASE_URL = URL.create(
    "postgresql+psycopg",
    username=os.getenv("DB_USER", "postgres"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT", "5432")),
    database=os.getenv("DB_NAME", "postgres"),
)

# pool_pre_ping: Supabase가 오래 쉬는 연결을 끊기 때문에, 연결을 빌려주기 전에 살아있는지 확인한다.
engine = create_engine(DATABASE_URL, pool_pre_ping=True, echo=False)

# expire_on_commit=False: commit 이후에도 메모리의 값을 그대로 쓴다 (응답을 만들 때 재조회 방지).
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


class Base(DeclarativeBase):
    """이 클래스를 상속하면 SQLAlchemy가 '이건 테이블이다'라고 인식한다."""


def get_db() -> Iterator[Session]:
    """요청 하나의 수명 동안 세션을 빌려주고, 응답이 나가면 자동으로 닫는다."""
    with SessionLocal() as session:
        yield session
