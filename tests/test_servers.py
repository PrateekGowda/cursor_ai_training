def test_add_server_requires_login(client):
    response = client.post(
        "/servers",
        data={"name": "web-01", "host": "10.0.0.1"},
        follow_redirects=False,
    )
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_add_list_and_delete_server(auth_client):
    add = auth_client.post(
        "/servers",
        data={
            "name": "web-01",
            "host": "10.0.0.12",
            "description": "demo host",
        },
        follow_redirects=True,
    )
    assert add.status_code == 200
    assert b"web-01" in add.data
    assert b"10.0.0.12" in add.data
    assert b"demo host" in add.data
    assert b"test123" not in add.data
    assert b"SECRET_KEY" not in add.data

    delete = auth_client.post("/servers/1/delete", follow_redirects=True)
    assert delete.status_code == 200
    assert b"Server removed." in delete.data
    assert b'data-server-id="1"' not in delete.data
    assert b"No servers yet" in delete.data



def test_add_server_validates_required_fields(auth_client):
    response = auth_client.post(
        "/servers",
        data={"name": "", "host": ""},
        follow_redirects=True,
    )
    assert b"Name and hostname/IP are required." in response.data
