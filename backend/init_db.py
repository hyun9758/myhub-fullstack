"""서버 시작 시 테이블 자동 생성 + RLS 잠금 + 초기 데이터 seed. package-by-feature 전환 후에도
Base.metadata 는 하나(db.py)를 공유하므로, 각 기능의 models 를 import 하기만 하면 등록된다."""

import argparse
from datetime import date

from sqlalchemy import inspect, select, text

from career.models.career import Career
from db import Base, SessionLocal, engine
from education.models.education import Education
from profiles.models.profile import Profile
from projects.models.project import Project
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
                    school="국내 4년제 대학교",
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
                institution="소프트웨어 개발 회사",
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


def seed_projects() -> None:
    with SessionLocal() as db:
        if db.scalars(select(Project)).first() is not None:
            return
        db.add_all(
            [
                Project(
                    category="팀 프로젝트",
                    year="2025",
                    period="2025.03 - 2025.11 (8개월)",
                    name="Q-Checker",
                    role="프론트엔드 & 백엔드 · 깃 마스터",
                    description="QR 코드 및 NFC 태그 기술을 활용한 QR 출석 관리 모바일 애플리케이션.",
                    links=[{"label": "GitHub", "url": "https://github.com/Capstone-project-syu/q-checker"}],
                ),
                Project(
                    category="개인 프로젝트",
                    year="2025",
                    period="2025.03 - 2025.11 (8개월)",
                    name="KAGE",
                    role="1인 풀스택 개발",
                    description="캐릭터를 생성하고 유저끼리 대화하는 캐릭터 대화 서비스.",
                    links=[
                        {"label": "GitHub", "url": "https://github.com/hyun9758/Kage"},
                        {"label": "Live", "url": "https://kage-seven.vercel.app/"},
                    ],
                ),
                Project(
                    category="팀 프로젝트",
                    year="2025",
                    period="2025.09 - 2025.11 (2개월)",
                    name="UnPlug",
                    role="프론트엔드 & 백엔드 · 깃 마스터",
                    description="도파민 디톡스를 돕는 모바일 애플리케이션.",
                    links=[{"label": "GitHub", "url": "https://github.com/BridgeON-Team/unplug"}],
                ),
                Project(
                    category="팀 프로젝트",
                    year="2025",
                    period="2025.02 - 2025.03 (1개월)",
                    name="FUNGLE",
                    role="프론트엔드 & 백엔드 · 팀장",
                    description="웹소설 주간 연재 및 도서 펀딩 커뮤니티 웹앱.",
                    links=[{"label": "GitHub", "url": "https://github.com/FRONT-END-BOOTCAMP-PLUS-3/fungle"}],
                ),
                Project(
                    category="팀 프로젝트",
                    year="2024",
                    period="2024.02 - 2024.03",
                    name="DOSIRAK",
                    role="프론트엔드",
                    description="멋쟁이사자처럼 프론트엔드 스쿨 팀 프로젝트.",
                    links=[
                        {"label": "GitHub", "url": "https://github.com/FRONTENDSCHOOL8/dosirak"},
                        {"label": "Live", "url": "https://hankki.netlify.app/"},
                    ],
                ),
            ]
        )
        db.commit()
        print("[init] project 초기 데이터 5건 입력")


def init_database() -> None:
    new_tables = create_tables()
    if new_tables:
        lock_down(new_tables)
        print(f"[init] 테이블 생성 + 잠금: {', '.join(new_tables)}")
    seed_profile()
    seed_education()
    seed_career()
    seed_skills()
    seed_projects()


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
