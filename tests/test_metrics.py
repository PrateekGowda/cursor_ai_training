def _add_server(client):
    client.post(
        "/servers",
        data={"name": "db-01", "host": "10.0.0.20", "description": ""},
    )


def test_metrics_requires_login(client):
    response = client.get("/api/servers/1/metrics", follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_metrics_shape_and_keys(auth_client):
    _add_server(auth_client)
    response = auth_client.get("/api/servers/1/metrics")
    assert response.status_code == 200
    data = response.get_json()
    assert data["simulated"] is True
    assert data["server_id"] == 1
    assert "cpu_percent" in data
    assert "used_gib" in data["memory"]
    assert "total_gib" in data["memory"]
    assert "in_mbps" in data["network"]
    assert "out_mbps" in data["network"]
    assert isinstance(data["listening_ports"], list)
    assert "password" not in data
    assert "SECRET_KEY" not in data
    body = response.get_data(as_text=True)
    assert "test123" not in body


def test_metrics_404_unknown_server(auth_client):
    response = auth_client.get("/api/servers/999/metrics")
    assert response.status_code == 404
    assert response.get_json()["error"] == "not found"
