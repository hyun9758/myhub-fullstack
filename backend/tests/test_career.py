from fastapi.testclient import TestClient

from main import app


def create_career(client, **overrides):
    payload = {
        "institution": "테스트회사",
        "period": "2020.01 ~ 2020.12",
        "role": "인턴",
        "description": "테스트 설명",
    }
    payload.update(overrides)
    response = client.post("/api/careers", json=payload)
    assert response.status_code == 201, response.text
    return response.json()


def test_list_careers_is_public_and_empty_by_default(client):
    response = client.get("/api/careers")
    assert response.status_code == 200
    assert response.json() == []


def test_create_career_without_auth_is_rejected(client):
    response = client.post(
        "/api/careers",
        json={"institution": "x", "period": "y", "role": "z"},
    )
    assert response.status_code == 401


def test_create_career_with_auth_succeeds(authed_client):
    body = create_career(authed_client)
    assert body["institution"] == "테스트회사"
    assert body["id"] is not None


def test_create_career_allows_description_to_be_omitted(authed_client):
    response = authed_client.post(
        "/api/careers",
        json={"institution": "무설명회사", "period": "2020", "role": "역할"},
    )
    assert response.status_code == 201
    assert response.json()["description"] is None


def test_list_careers_returns_created_items_ordered_by_period_desc(authed_client):
    create_career(authed_client, institution="먼저", period="2010.01 ~ 2010.12")
    create_career(authed_client, institution="나중", period="2020.01 ~ 2020.12")

    response = authed_client.get("/api/careers")
    institutions = [item["institution"] for item in response.json()]
    assert institutions == ["나중", "먼저"]


def test_update_career_without_auth_is_rejected(authed_client):
    created = create_career(authed_client)
    payload = {"institution": "수정됨", "period": "2020", "role": "역할"}
    anonymous_client = TestClient(app)
    response = anonymous_client.put(f"/api/careers/{created['id']}", json=payload)
    assert response.status_code == 401


def test_update_career_with_auth_succeeds(authed_client):
    created = create_career(authed_client)
    payload = {"institution": "수정된 회사", "period": "2021", "role": "정규직", "description": None}
    response = authed_client.put(f"/api/careers/{created['id']}", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["institution"] == "수정된 회사"
    assert body["description"] is None


def test_update_career_nonexistent_returns_404(authed_client):
    payload = {"institution": "x", "period": "y", "role": "z"}
    response = authed_client.put("/api/careers/999999", json=payload)
    assert response.status_code == 404


def test_delete_career_without_auth_is_rejected(authed_client):
    created = create_career(authed_client)
    anonymous_client = TestClient(app)
    response = anonymous_client.delete(f"/api/careers/{created['id']}")
    assert response.status_code == 401


def test_delete_career_with_auth_succeeds(authed_client):
    created = create_career(authed_client)
    response = authed_client.delete(f"/api/careers/{created['id']}")
    assert response.status_code == 204

    list_response = authed_client.get("/api/careers")
    assert all(item["id"] != created["id"] for item in list_response.json())


def test_delete_career_nonexistent_returns_404(authed_client):
    response = authed_client.delete("/api/careers/999999")
    assert response.status_code == 404
