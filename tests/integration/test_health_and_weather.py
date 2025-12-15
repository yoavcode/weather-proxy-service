from app.main import app


def test_health_ok():
    client = app.test_client()
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"
    assert "X-Request-ID" in resp.headers


def test_weather_requires_city():
    client = app.test_client()
    resp = client.get("/weather")
    assert resp.status_code == 400
    assert resp.get_json()["error"] == "city query param is required"
    assert "X-Request-ID" in resp.headers
