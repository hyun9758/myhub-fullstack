def test_get_profile_returns_404_when_none_seeded(client):
    response = client.get("/api/profile")
    assert response.status_code == 404


def test_get_profile_returns_seeded_profile(client, seeded_profile):
    response = client.get("/api/profile")
    assert response.status_code == 200
    body = response.json()["profile"]
    assert body["full_name"] == "테스트 사용자"
    assert body["headline"] == "백엔드 개발자"


def test_update_profile_without_auth_is_rejected(client, seeded_profile):
    payload = {"full_name": "정현수", "headline": "개발자", "summary": "소개"}
    response = client.put("/api/profile", json=payload)
    assert response.status_code == 401


def test_update_profile_with_auth_succeeds_and_persists(authed_client, seeded_profile):
    payload = {"full_name": "정현수", "headline": "Front-End Developer", "summary": "새 소개"}
    response = authed_client.put("/api/profile", json=payload)
    assert response.status_code == 200
    body = response.json()["profile"]
    assert body["full_name"] == "정현수"
    assert body["headline"] == "Front-End Developer"

    # 저장 후 다시 조회해도 값이 그대로 반영되어 있어야 한다.
    get_response = authed_client.get("/api/profile")
    assert get_response.json()["profile"]["full_name"] == "정현수"


def test_update_profile_without_seeded_row_returns_404(authed_client):
    payload = {"full_name": "정현수", "headline": "개발자", "summary": None}
    response = authed_client.put("/api/profile", json=payload)
    assert response.status_code == 404
