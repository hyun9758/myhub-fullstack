# MyHub Full-Stack (Day 2)

React + TypeScript(Vite) 프론트엔드 · FastAPI 백엔드 · SQLAlchemy ORM · Supabase(PostgreSQL) 기반의 풀스택 CV 애플리케이션입니다. Day 1의 정적 CV(`cv-myhub`)를 서버/DB를 갖춘 풀스택으로 확장합니다.

## 구조

```
myhub_02_fullstack/
├── backend/     FastAPI 서버 (Step 1~7)
├── frontend/    React + TS + Vite 프론트엔드
└── docs/        PRD, 요구사항 그릴링, 데이터 스키마 등 명세 산출물
```

## 진행 상태 (스캐폴딩 Step 1-7)

- [x] Step 1 — 백엔드 ↔ Supabase 연결 확인 (`GET /health`)
- [x] Step 2 — `profile` 테이블 생성(RLS 잠금) 및 `GET /api/profile`
- [x] Step 3 — 프론트엔드 화면 붙이기 (Vite 프록시 + openapi-typescript 자동 생성 타입)
- [ ] Step 4 — 로그인 및 In-place 편집
- [ ] Step 5 — SQLAlchemy ORM 도입
- [ ] Step 6 — package-by-feature 재구성 (profiles/education/auth)
- [ ] Step 7 — pytest 테스트

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

## 환경 변수

`backend/.env.example`을 참고해 `backend/.env`를 채웁니다 (git에 올라가지 않음). Supabase 대시보드 → Project Settings → Database → Connect → Session pooler에서 접속 정보를 확인합니다.
