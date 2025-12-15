from unittest.mock import Mock, patch
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


def test_weather_success_returns_200_mocked_upstream():
    client = app.test_client()

    fake_resp = Mock()
    fake_resp.raise_for_status.return_value = None
    fake_resp.json.return_value = {"current_weather": {"temperature": 25.0}}

    with patch("app.weather_provider.requests.get", return_value=fake_resp) as mock_get:
        resp = client.get("/weather?city=Tel%20Aviv")

    assert resp.status_code == 200
    data = resp.get_json()
    assert data["city"] == "Tel Aviv"
    assert data["provider"] == "open-meteo"
    assert data["data"]["temperature"] == 25.0
    assert "X-Request-ID" in resp.headers

    mock_get.assert_called_once()
