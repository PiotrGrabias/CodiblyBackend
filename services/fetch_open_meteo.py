import httpx


async def fetch_open_meteo(latitude: float, longitude: float):
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "daily": [
                "temperature_2m_min",
                "temperature_2m_max",
                "weathercode",
                "precipitation_sum",
                "sunshine_duration",
                "pressure_msl"
            ],
            "timezone": "auto"
        }
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, params=params)
            resp.raise_for_status()
            return resp.json()
    except httpx.HTTPStatusError as e:
        raise Exception(f"API Error: {e.response.status_code}")
    except httpx.RequestError:
        raise Exception("Can't connect with API")

