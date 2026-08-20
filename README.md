# MyHub Full-Stack (Day 2)

React + TypeScript(Vite) 프론트엔드 · FastAPI 백엔드 · SQLAlchemy ORM · Supabase(PostgreSQL) 기반의 풀스택 CV 애플리케이션입니다. Day 1의 정적 CV(`cv-myhub`)를 서버/DB를 갖춘 풀스택으로 확장합니다.

## 구조

```
myhub_02_fullstack/
├── backend/
│   ├── auth/          로그인 · 세션 확인 · 로그아웃 (DB 없음, 비밀번호는 .env)
│   ├── profiles/      프로필 조회 · 수정 (Read + Update, 단일 레코드)
│   ├── education/     학력 CRUD (여러 건)
│   │   └── (각 기능 폴더는 router → service → repository → models 4겹 구조)
│   ├── tests/         pytest (기능별 테스트 파일 + conftest 픽스처)
│   ├── db.py          SQLAlchemy 엔진 · 세션 · Base
│   ├── init_db.py     서버 시작 시 테이블 자동 생성 + RLS 잠금 + seed
│   ├── schemas.py     기능 하나에 속하지 않는 공용 DTO (HealthResponse)
│   └── main.py        FastAPI 앱 조립 (라우터 include)
├── frontend/
│   └── src/
│       ├── features/{auth,profile,education}/   백엔드와 동일한 기능별 구조
│       ├── theme/      다크모드 (useTheme, ThemeToggle)
│       └── api/        httpClient, openapi-typescript 자동 생성 타입
└── docs/               PRD, 요구사항 그릴링, 데이터 스키마 등 명세 산출물
```

## 진행 상태 (스캐폴딩 Step 1-7)

- [x] Step 1 — 백엔드 ↔ Supabase 연결 확인 (`GET /health`)
- [x] Step 2 — `profile` 테이블 생성(RLS 잠금) 및 `GET /api/profile`
- [x] Step 3 — 프론트엔드 화면 붙이기 (Vite 프록시 + openapi-typescript 자동 생성 타입)
- [x] Step 4 — 로그인(서명 세션 쿠키) 및 In-place 편집, 세션 만료 시 자동 로그인 유도
- [x] Step 5 — SQLAlchemy ORM 도입 (`db.py`/`models.py`/`schemas.py`/`init_db.py` 분리, 서버 시작 시 테이블 자동 생성+seed)
- [x] Step 6 — package-by-feature 재구성 (auth/profiles/education), education CRUD, 다크모드+디자인 토큰
- [x] Step 7 — pytest 테스트 (23개, 커버리지 87%, 임시 SQLite로 실제 DB 미사용)

## 로컬 실행

**백엔드**
```bash
cd backend
source .venv/bin/activate   # Windows: .venv\Scripts\activate
uvicorn main:app --reload --port 8080
```

**프론트엔드**
```bash
cd frontend
npm run dev -- --port 5173
```

## 테스트

```bash
cd backend
source .venv/bin/activate
pip install -r requirements-dev.txt
python -m pytest
```

- `tests/conftest.py`가 `.env`의 실제 Supabase 대신 임시 SQLite로 바꿔치기하므로 실제 DB에는 영향이 없습니다.
- 실행 후 `htmlcov/index.html`을 브라우저로 열면 파일별 커버리지(어떤 줄이 실행되지 않았는지)를 확인할 수 있습니다.
- `init_db.py`의 커버리지가 낮은 것은 정상입니다 — 테스트는 매 테스트마다 빈 스키마로 격리하기 위해 앱의 `lifespan`(시작 시 자동 seed)을 일부러 트리거하지 않습니다.

## 환경 변수

`backend/.env.example`을 참고해 `backend/.env`를 채웁니다 (git에 올라가지 않음). Supabase 대시보드 → Project Settings → Database → Connect → Session pooler에서 접속 정보를 확인합니다.
