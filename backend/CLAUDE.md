# backend

FastAPI + SQLAlchemy, package-by-feature.

## 새 기능 추가할 때

1. `feature/models/feature.py` — SQLAlchemy 엔티티. 기본키는 `Identity()`가 아니라 `Integer, primary_key=True, autoincrement=True`를 쓴다 (SQLite 테스트 호환성 때문 — `docs`... 실은 `education/models/education.py`의 주석 참고).
2. `feature/schemas.py` — Pydantic DTO (`FeatureDTO`, `FeatureCreateRequest`, `FeatureUpdateRequest`).
3. `feature/repository.py` — ORM 쿼리만.
4. `feature/service.py` — 업무 규칙(404 등), HTTP는 모른다.
5. `feature/router.py` — 엔드포인트. 쓰기 엔드포인트는 `Depends(require_auth)`(auth.service)를 단다. 읽기 전용으로 인증에 따라 응답을 바꿔야 하면 `Depends(optional_auth)`를 쓴다 (profiles의 민감 필드 마스킹 참고).
6. `main.py`에 라우터 `include_router` 추가.
7. `init_db.py`에 `seed_<feature>()` 추가하고 `init_database()`에서 호출.
8. 실제 DB(Supabase)에 이미 존재하는 테이블에 컬럼을 추가했다면 `Base.metadata.create_all()`은 컬럼을 만들어주지 않는다 — `psycopg`로 직접 `ALTER TABLE ... ADD COLUMN IF NOT EXISTS`를 실행해야 한다 (임시 스크립트를 만들어 실행 후 삭제하는 방식을 씀).

## 인증

`auth/service.py`의 세션은 서명된 쿠키(itsdangerous) 기반, 유효기간 7일(PRD TR-11). `require_auth`는 401로 차단, `optional_auth`는 bool만 반환(차단하지 않음).

## 테스트

```bash
pip install -r requirements-dev.txt
python -m pytest
```

`tests/conftest.py`가 `DATABASE_URL`을 임시 SQLite로 바꿔치기하므로 `.env`의 실제 Supabase는 건드리지 않는다.
