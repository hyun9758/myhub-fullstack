from fastapi.testclient import TestClient

from main import app


def create_project(client, **overrides):
    payload = {
        "category": "팀 프로젝트",
        "year": "2020",
        "period": "2020.01 - 2020.06",
        "name": "테스트프로젝트",
        "role": "역할",
        "description": "테스트 설명",
        "links": [{"label": "GitHub", "url": "https://example.com/repo"}],
    }
    payload.update(overrides)
    response = client.post("/api/projects", json=payload)
    assert response.status_code == 201, response.text
    return response.json()


def test_list_projects_is_public_and_empty_by_default(client):
    response = client.get("/api/projects")
    assert response.status_code == 200
    assert response.json() == []


def test_create_project_without_auth_is_rejected(client):
    response = client.post(
        "/api/projects",
        json={"category": "x", "year": "2020", "name": "y", "role": "z"},
    )
    assert response.status_code == 401


def test_create_project_with_auth_succeeds(authed_client):
    body = create_project(authed_client)
    assert body["name"] == "테스트프로젝트"
    assert body["links"][0]["label"] == "GitHub"


def test_create_project_allows_optional_fields_to_be_omitted(authed_client):
    response = authed_client.post(
        "/api/projects",
        json={"category": "개인 프로젝트", "year": "2020", "name": "미니멀", "role": "개발"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["period"] is None
    assert body["description"] is None
    assert body["links"] == []


def test_create_project_rejects_invalid_link_url(authed_client):
    response = authed_client.post(
        "/api/projects",
        json={
            "category": "팀 프로젝트",
            "year": "2020",
            "name": "x",
            "role": "y",
            "links": [{"label": "GitHub", "url": "not-a-url"}],
        },
    )
    assert response.status_code == 422


def test_list_projects_returns_created_items_ordered_by_year_desc(authed_client):
    create_project(authed_client, name="오래된 프로젝트", year="2018")
    create_project(authed_client, name="최신 프로젝트", year="2025")

    response = authed_client.get("/api/projects")
    names = [item["name"] for item in response.json()]
    assert names == ["최신 프로젝트", "오래된 프로젝트"]


def test_update_project_without_auth_is_rejected(authed_client):
    created = create_project(authed_client)
    payload = {"category": "x", "year": "2020", "name": "수정됨", "role": "y"}
    anonymous_client = TestClient(app)
    response = anonymous_client.put(f"/api/projects/{created['id']}", json=payload)
    assert response.status_code == 401


def test_update_project_with_auth_succeeds(authed_client):
    created = create_project(authed_client)
    payload = {"category": "개인 프로젝트", "year": "2021", "name": "수정된 이름", "role": "역할2"}
    response = authed_client.put(f"/api/projects/{created['id']}", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "수정된 이름"
    assert body["links"] == []


def test_update_project_nonexistent_returns_404(authed_client):
    payload = {"category": "x", "year": "2020", "name": "y", "role": "z"}
    response = authed_client.put("/api/projects/999999", json=payload)
    assert response.status_code == 404


def test_delete_project_without_auth_is_rejected(authed_client):
    created = create_project(authed_client)
    anonymous_client = TestClient(app)
    response = anonymous_client.delete(f"/api/projects/{created['id']}")
    assert response.status_code == 401


def test_delete_project_with_auth_succeeds(authed_client):
    created = create_project(authed_client)
    response = authed_client.delete(f"/api/projects/{created['id']}")
    assert response.status_code == 204

    list_response = authed_client.get("/api/projects")
    assert all(item["id"] != created["id"] for item in list_response.json())


def test_delete_project_nonexistent_returns_404(authed_client):
    response = authed_client.delete("/api/projects/999999")
    assert response.status_code == 404
