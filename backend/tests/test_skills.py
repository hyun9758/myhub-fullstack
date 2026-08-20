"""skills는 profile과 마찬가지로 단일형(singleton)이라, seed가 없는 빈 스키마에서는
GET/PUT 모두 404를 반환한다 (conftest의 client 픽스처는 lifespan seed를 트리거하지 않음)."""

from db import SessionLocal
from skills.models.skills import Skills


def seed_skills():
    with SessionLocal() as db:
        entity = Skills(tech=["Python", "TypeScript"], languages=[{"name": "한국어", "level": "모국어"}])
        db.add(entity)
        db.commit()


def test_get_skills_returns_404_when_none_seeded(client):
    response = client.get("/api/skills")
    assert response.status_code == 404


def test_get_skills_returns_seeded_data(client):
    seed_skills()
    response = client.get("/api/skills")
    assert response.status_code == 200
    body = response.json()
    assert body["tech"] == ["Python", "TypeScript"]
    assert body["languages"] == [{"name": "한국어", "level": "모국어"}]


def test_update_skills_without_auth_is_rejected(client):
    seed_skills()
    payload = {"tech": ["Go"], "languages": []}
    response = client.put("/api/skills", json=payload)
    assert response.status_code == 401


def test_update_skills_with_auth_succeeds_and_persists(authed_client):
    seed_skills()
    payload = {"tech": ["Rust", "Go"], "languages": [{"name": "영어", "level": "업무 가능"}]}
    response = authed_client.put("/api/skills", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["tech"] == ["Rust", "Go"]

    get_response = authed_client.get("/api/skills")
    assert get_response.json()["tech"] == ["Rust", "Go"]


def test_update_skills_replaces_whole_lists_not_merges(authed_client):
    seed_skills()
    # tech 목록을 완전히 새 값으로 교체 — 기존 "Python"이 남아있지 않아야 한다 (통째 저장, DRQ-016).
    response = authed_client.put("/api/skills", json={"tech": ["Only-This"], "languages": []})
    assert response.status_code == 200
    assert response.json()["tech"] == ["Only-This"]


def test_update_skills_without_seeded_row_returns_404(authed_client):
    response = authed_client.put("/api/skills", json={"tech": [], "languages": []})
    assert response.status_code == 404
