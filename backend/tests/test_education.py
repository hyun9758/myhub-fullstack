from fastapi.testclient import TestClient

from main import app


def create_education(client, **overrides):
    payload = {
        "school": "테스트대학교",
        "degree": "학사",
        "field_of_study": "컴퓨터공학",
        "start_date": "2020-03-01",
        "end_date": "2024-02-28",
    }
    payload.update(overrides)
    response = client.post("/api/educations", json=payload)
    assert response.status_code == 201, response.text
    return response.json()


def test_list_educations_is_public_and_empty_by_default(client):
    response = client.get("/api/educations")
    assert response.status_code == 200
    assert response.json() == []


def test_create_education_without_auth_is_rejected(client):
    response = client.post(
        "/api/educations",
        json={"school": "x", "degree": "y", "start_date": "2020-01-01"},
    )
    assert response.status_code == 401


def test_create_education_with_auth_succeeds(authed_client):
    body = create_education(authed_client)
    assert body["school"] == "테스트대학교"
    assert body["id"] is not None


def test_create_education_allows_optional_fields_to_be_omitted(authed_client):
    response = authed_client.post(
        "/api/educations",
        json={"school": "무학과", "degree": "학사", "start_date": "2020-01-01"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["field_of_study"] is None
    assert body["end_date"] is None


def test_list_educations_returns_created_items_ordered_by_start_date_desc(authed_client):
    create_education(authed_client, school="먼저 입학", start_date="2010-03-01", end_date="2014-02-28")
    create_education(authed_client, school="나중 입학", start_date="2020-03-01", end_date="2024-02-28")

    response = authed_client.get("/api/educations")
    schools = [item["school"] for item in response.json()]
    assert schools == ["나중 입학", "먼저 입학"]


def test_update_education_without_auth_is_rejected(authed_client):
    created = create_education(authed_client)
    payload = {"school": "수정됨", "degree": "학사", "start_date": "2020-03-01"}
    # 세션 쿠키가 없는 별도의(로그인 안 된) 클라이언트로 같은 요청을 보낸다.
    anonymous_client = TestClient(app)
    response = anonymous_client.put(f"/api/educations/{created['id']}", json=payload)
    assert response.status_code == 401


def test_update_education_with_auth_succeeds(authed_client):
    created = create_education(authed_client)
    payload = {
        "school": "수정된 학교",
        "degree": "석사",
        "field_of_study": "인공지능",
        "start_date": "2020-03-01",
        "end_date": None,
    }
    response = authed_client.put(f"/api/educations/{created['id']}", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["school"] == "수정된 학교"
    assert body["degree"] == "석사"
    assert body["end_date"] is None


def test_update_education_nonexistent_returns_404(authed_client):
    payload = {"school": "x", "degree": "y", "start_date": "2020-01-01"}
    response = authed_client.put("/api/educations/999999", json=payload)
    assert response.status_code == 404


def test_delete_education_without_auth_is_rejected(authed_client):
    created = create_education(authed_client)
    anonymous_client = TestClient(app)
    response = anonymous_client.delete(f"/api/educations/{created['id']}")
    assert response.status_code == 401


def test_delete_education_with_auth_succeeds(authed_client):
    created = create_education(authed_client)
    response = authed_client.delete(f"/api/educations/{created['id']}")
    assert response.status_code == 204

    list_response = authed_client.get("/api/educations")
    assert all(item["id"] != created["id"] for item in list_response.json())


def test_delete_education_nonexistent_returns_404(authed_client):
    response = authed_client.delete("/api/educations/999999")
    assert response.status_code == 404
