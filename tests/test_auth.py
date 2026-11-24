from werkzeug.security import check_password_hash


def test_successful_login(client):
    response = client.post(
        "/login",
        data={"username": "admin", "password": "test123"},
        follow_redirects=False,
    )
    assert response.status_code == 302
    assert "/dashboard" in response.headers["Location"]
    follow = client.get("/dashboard")
    assert follow.status_code == 200
    assert b"Linux servers" in follow.data


def test_failed_login_generic_message(client):
    response = client.post(
        "/login",
        data={"username": "admin", "password": "not-the-password"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Invalid username or password." in response.data
    assert b"not-the-password" not in response.data


def test_logout_clears_session(auth_client):
    assert auth_client.get("/dashboard").status_code == 200
    response = auth_client.post("/logout", follow_redirects=False)
    assert response.status_code == 302
    protected = auth_client.get("/dashboard", follow_redirects=False)
    assert protected.status_code == 302
    assert "/login" in protected.headers["Location"]


def test_protected_route_redirects(client):
    response = client.get("/dashboard", follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_password_stored_as_hash(app, client):
    stored = app.config["ADMIN_PASSWORD_HASH"]
    assert stored != "test123"
    assert check_password_hash(stored, "test123")
    assert not check_password_hash(stored, "wrong")

    login_page = client.get("/login")
    assert stored.encode() not in login_page.data

    bad = client.post(
        "/login",
        data={"username": "admin", "password": "secret-attempt"},
        follow_redirects=True,
    )
    assert b"secret-attempt" not in bad.data
    assert b"Invalid username or password." in bad.data
    assert stored.encode() not in bad.data
