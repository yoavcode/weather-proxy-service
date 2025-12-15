import requests
from tenacity import retry, stop_after_attempt, wait_fixed


class WeatherProviderError(Exception):
    pass


@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
def fetch_weather(city: str) -> dict:
    try:
        resp = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": 0,
                "longitude": 0,
                "current_weather": True,
            },
            timeout=5,
        )
        resp.raise_for_status()
        return {
            "city": city,
            "provider": "open-meteo",
            "data": resp.json().get("current_weather"),
        }
    except Exception as exc:
        raise WeatherProviderError(str(exc))
