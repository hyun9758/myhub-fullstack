"""테스트 전용 환경. 실제 .env(Supabase) 대신 임시 SQLite를 쓰고, 테스트마다 스키마를 초기화한다.

주의: 환경변수를 설정하는 코드가 db/main 의 import 보다 반드시 먼저 와야 한다.
db.py 는 모듈을 불러오는 순간(import time) DATABASE_URL 을 읽어 엔진을 만들기 때문이다.
"""

import os
import tempfile
from pathlib import Path

import pytest

TEST_DB_DIR = tempfile.mkdtemp(prefix="myhub_pytest_")
TEST_DB_PATH = Path(TEST_DB_DIR, "test.db").as_posix()

os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB_PATH}"
os.environ["ADMIN_PASSCODE"] = "test-admin-passcode"
os.environ["SESSION_SECRET"] = "test-session-secret"

from fastapi.testclient import TestClient  # noqa: E402

from db import Base, engine  # noqa: E402
from education.models.education import Education  # noqa: E402,F401  (Base.metadata 등록용)
from main import app  # noqa: E402
from profiles.models.profile import Profile  # noqa: E402,F401  (Base.metadata 등록용)

ADMIN_PASSCODE = os.environ["ADMIN_PASSCODE"]


@pytest.fixture(autouse=True)
def _reset_database():
    """모든 테스트 앞에 자동으로 끼어들어, 매번 깨끗하고 빈 스키마를 보장한다."""
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield


@pytest.fixture()
def admin_passcode():
    return ADMIN_PASSCODE


@pytest.fixture()
def client():
    # 일부러 `with` 컨텍스트로 열지 않는다 — lifespan(=init_database, 초기 데이터 seed)이
    # 트리거되지 않게 해서, 각 테스트가 매번 "정말로 빈" 스키마에서 시작하게 만들기 위해서다.
    return TestClient(app)


@pytest.fixture()
def authed_client(client):
    response = client.post("/api/auth/session", json={"passcode": ADMIN_PASSCODE})
    assert response.status_code == 200
    return client


@pytest.fixture()
def seeded_profile():
    """profile 관련 테스트를 위해, 라우터를 거치지 않고 직접 한 건을 심어둔다."""
    from db import SessionLocal

    with SessionLocal() as db:
        entity = Profile(full_name="테스트 사용자", headline="백엔드 개발자", summary="테스트용 소개")
        db.add(entity)
        db.commit()
        db.refresh(entity)
        return entity.id
