# MyHub Full-Stack

풀스택 개인 이력서(CV) 웹앱. React+TS(Vite) 프론트엔드, FastAPI 백엔드, SQLAlchemy ORM, Supabase(PostgreSQL).

## 실행

```bash
# backend (backend/ 안에서)
source .venv/bin/activate && uvicorn main:app --reload --port 8080

# frontend (frontend/ 안에서)
npm run dev
```

## 구조 규약

- **package-by-feature**: 백엔드는 `auth/`, `profiles/`, `education/`, `career/`, `skills/`처럼 기능별 폴더에 `router.py → service.py → repository.py → models/` 4겹을 갖는다. 새 기능도 이 틀을 그대로 복제한다.
- 프론트엔드는 `src/features/{auth,profile,education,career,skills}/`가 백엔드 구조를 그대로 반영한다.
- API 타입은 손으로 쓰지 않는다 — 백엔드를 띄운 뒤 `frontend`에서 `npm run gen:api`로 `src/api/schema.d.ts`를 재생성한다.
- `.env`, `.env.example`은 직접 수정하지 않는다 (`.claude/hooks/protect-env.sh`가 차단함). 값이 필요하면 사용자에게 요청한다.

## 명세 문서 (읽는 순서)

1. `specs/myhub_prd.md` — 제품 요구사항 (v0.4, 그릴링 반영)
2. `specs/analysis/myhub_us.md` — 유저스토리 + 인수 조건
3. `specs/design/myhub_data_req_er.md` — 논리 데이터 모델 (구현 시 이 문서를 우선 참고)
4. `specs/design/myhub_uiux_req.md` — 디자인 시스템
5. `specs/adr/` — 되돌리기 어려운 결정과 그 이유
6. `CONTEXT.md` — 프로젝트 용어집

## 이번 사이클 구현 범위

profile / education / career / skills / projects 5개 도메인이 구현되어 있다 (intro/publications/awards는 여전히 범위 밖, `myhub_us.md` §0.2 참고).

## 테스트

`backend/tests/`에 pytest 스위트가 있다(55개, 커버리지 90%, `python -m pytest`). coding-agent 역할의 구현 작업(7.5)은 테스트를 작성하지 않는다 — 테스트는 8.1처럼 별도 단계에서 명시적으로 요청했을 때만 작성한다.
