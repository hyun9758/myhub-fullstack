"""서버 시작 시 테이블 자동 생성 + RLS 잠금 + 초기 데이터 seed. package-by-feature 전환 후에도
Base.metadata 는 하나(db.py)를 공유하므로, 각 기능의 models 를 import 하기만 하면 등록된다."""

import argparse
from datetime import date

from sqlalchemy import inspect, select, text

from career.models.career import Career
from db import Base, SessionLocal, engine
from education.models.education import Education
from profiles.models.profile import Profile
from skills.models.skills import Skills


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


def seed_profile() -> None:
    with SessionLocal() as db:
        if db.scalars(select(Profile)).first() is not None:
            return
        db.add(
            Profile(
                full_name="정현수",
                headline="Front-End & Full-Stack Developer",
                summary=(
                    "React·Next.js·React Native를 기반으로 프론트엔드부터 백엔드, "
                    "모바일까지 아우르는 풀스택 웹/앱 개발 경험을 쌓아온 개발자입니다."
                ),
            )
        )
        db.commit()
        print("[init] profile 초기 데이터 1건 입력")


def seed_education() -> None:
    with SessionLocal() as db:
        if db.scalars(select(Education)).first() is not None:
            return
        db.add_all(
            [
                Education(
                    school="삼육대학교",
                    degree="학사",
                    field_of_study="컴퓨터공학과 소프트웨어공학부",
                    start_date=date(2020, 3, 1),
                    end_date=date(2026, 2, 28),
                ),
                Education(
                    school="멋쟁이사자처럼 프론트엔드 스쿨 8기",
                    degree="수료",
                    field_of_study="프론트엔드 부트캠프",
                    start_date=date(2023, 10, 1),
                    end_date=date(2024, 3, 31),
                ),
                Education(
                    school="멋쟁이사자처럼 플러스 프론트엔드 3기",
                    degree="수료",
                    field_of_study="프론트엔드 심화 과정",
                    start_date=date(2025, 1, 1),
                    end_date=date(2025, 3, 31),
                ),
            ]
        )
        db.commit()
        print("[init] education 초기 데이터 3건 입력")


def seed_career() -> None:
    with SessionLocal() as db:
        if db.scalars(select(Career)).first() is not None:
            return
        db.add(
            Career(
                institution="㈜모디엠",
                period="2025.12 ~ 2026.02",
                role="내비게이션 SW 개발 QA",
                description=None,
            )
        )
        db.commit()
        print("[init] career 초기 데이터 1건 입력")


def seed_skills() -> None:
    with SessionLocal() as db:
        if db.scalars(select(Skills)).first() is not None:
            return
        db.add(
            Skills(
                tech=[
                    "HTML5", "JavaScript", "TypeScript", "React", "CSS3",
                    "Styled-Components", "TailwindCSS", "Next.js", "Spring", "JWT",
                    "React Native", "Expo", "PostgreSQL", "MySQL", "Supabase", "Prisma",
                    "AWS", "Docker", "Node.js", "FastAPI", "SQLAlchemy",
                ],
                languages=[
                    {"name": "한국어", "level": "모국어"},
                    {"name": "영어", "level": "업무 가능"},
                ],
            )
        )
        db.commit()
        print("[init] skills 초기 데이터 1건 입력")


def init_database() -> None:
    new_tables = create_tables()
    if new_tables:
        lock_down(new_tables)
        print(f"[init] 테이블 생성 + 잠금: {', '.join(new_tables)}")
    seed_profile()
    seed_education()
    seed_career()
    seed_skills()


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
