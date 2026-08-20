def test_session_check_without_login_returns_false(client):
    response = client.get("/api/auth/session")
    assert response.status_code == 200
    assert response.json() == {"authenticated": False}


def test_login_with_wrong_passcode_returns_401(client):
    response = client.post("/api/auth/session", json={"passcode": "wrong"})
    assert response.status_code == 401


def test_login_with_correct_passcode_succeeds(client, admin_passcode):
    response = client.post("/api/auth/session", json={"passcode": admin_passcode})
    assert response.status_code == 200
    assert response.json() == {"authenticated": True}


def test_session_check_after_login_returns_true(authed_client):
    response = authed_client.get("/api/auth/session")
    assert response.status_code == 200
    assert response.json() == {"authenticated": True}


def test_logout_clears_session(authed_client):
    logout_response = authed_client.delete("/api/auth/session")
    assert logout_response.status_code == 200
    assert logout_response.json() == {"authenticated": False}

    check_response = authed_client.get("/api/auth/session")
    assert check_response.json() == {"authenticated": False}
