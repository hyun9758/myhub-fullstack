"""서버 시작 시 테이블 자동 생성 + RLS 잠금 + 초기 데이터 seed."""

import argparse

from sqlalchemy import inspect, select, text

import models  # noqa: F401  (Base.metadata 에 등록되도록 import 필요)
from db import Base, SessionLocal, engine


def create_tables() -> list[str]:
    """새로 만들어진 테이블 이름 목록을 돌려준다."""
    before = set(inspect(engine).get_table_names(schema="public"))
    Base.metadata.create_all(engine)  # checkfirst=True 가 기본값이라 없는 테이블만 만든다.
    after = set(inspect(engine).get_table_names(schema="public"))
    return sorted(after - before)


def lock_down(table_names: list[str]) -> None:
    with engine.begin() as conn:
        for name in table_names:
            conn.execute(text(f'alter table public."{name}" enable row level security'))
            conn.execute(text(f'revoke all on table public."{name}" from anon, authenticated'))


def seed() -> None:
    with SessionLocal() as db:
        if db.scalars(select(models.Profile)).first() is not None:
            return
        db.add(
            models.Profile(
                full_name="정현수",
                headline="Front-End & Full-Stack Developer",
                summary=(
                    "React·Next.js·React Native를 기반으로 프론트엔드부터 백엔드, "
                    "모바일까지 아우르는 풀스택 웹/앱 개발 경험을 쌓아온 개발자입니다."
                ),
            )
        )
        db.commit()
        print("[init] 초기 데이터 1건 입력")


def init_database() -> None:
    new_tables = create_tables()
    if new_tables:
        lock_down(new_tables)
        print(f"[init] 테이블 생성 + 잠금: {', '.join(new_tables)}")
    seed()


def reset() -> None:
    Base.metadata.drop_all(engine)
    init_database()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="기존 테이블을 지우고 다시 만든다.")
    args = parser.parse_args()

    if args.reset:
        reset()
    else:
        init_database()
