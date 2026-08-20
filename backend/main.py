"""MyHub backend — FastAPI 앱 조립. 각 기능의 라우터를 여기서 include 하기만 한다
(package-by-feature: 기능 관련 로직은 각 패키지의 router/service/repository 안에 있다)."""

from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from auth.router import router as auth_router
from career.router import router as career_router
from db import engine, get_db
from education.router import router as education_router
from init_db import init_database
from profiles.router import router as profiles_router
from projects.router import router as projects_router
from schemas import HealthResponse
from skills.router import router as skills_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 엔티티 기준으로 테이블이 있는지 확인하고, 없으면 만든다. 비어 있으면 초기 데이터를 넣는다.
    init_database()
    yield
    engine.dispose()


app = FastAPI(title="MyHub Backend", lifespan=lifespan)

app.include_router(auth_router)
app.include_router(profiles_router)
app.include_router(education_router)
app.include_router(career_router)
app.include_router(projects_router)
app.include_router(skills_router)


@app.get("/health", response_model=HealthResponse)
def health(db: Session = Depends(get_db)):
    """Supabase(PostgreSQL) 연결 상태와 버전 정보를 반환한다. (raw SQL — 엔티티로 표현할 대상이 아님)"""
    try:
        version = db.scalar(text("select version()"))
        return HealthResponse(database="연결됨", postgres_version=version)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"DB 연결 실패: {e}")
