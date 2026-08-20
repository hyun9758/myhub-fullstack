"""`/health`는 select version()(PostgreSQL 전용 함수)을 실행하므로 테스트용 SQLite로는
흉내 낼 수 없다. FastAPI의 dependency_overrides로 get_db 자체를 가짜 세션으로 바꿔치기한다."""

from unittest.mock import MagicMock

from sqlalchemy.exc import OperationalError

from db import get_db
from main import app


def test_health_returns_200_and_version_when_database_reachable(client):
    fake_session = MagicMock()
    fake_session.scalar.return_value = "PostgreSQL 17.6 (fake)"

    def fake_get_db():
        yield fake_session

    app.dependency_overrides[get_db] = fake_get_db

    try:
        response = client.get("/health")
    finally:
        app.dependency_overrides.pop(get_db, None)

    assert response.status_code == 200
    body = response.json()
    assert body["database"] == "연결됨"
    assert body["postgres_version"] == "PostgreSQL 17.6 (fake)"


def test_health_returns_502_when_database_unreachable(client):
    fake_session = MagicMock()
    fake_session.scalar.side_effect = OperationalError("select version()", {}, Exception("connection refused"))

    def fake_get_db():
        yield fake_session

    app.dependency_overrides[get_db] = fake_get_db

    try:
        response = client.get("/health")
    finally:
        app.dependency_overrides.pop(get_db, None)

    assert response.status_code == 502
