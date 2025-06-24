from models.weather_forecast import WeatherForecast
from models.weekly_summary import WeeklySummary
from services.fetch_open_meteo import fetch_open_meteo
from utils import calculate_energy


def build_forecast(data: dict) -> list[WeatherForecast]:
    forecasts = []
    for i in range(7):
        forecasts.append(WeatherForecast(
            date=data["daily"]["time"][i],
            weather_code=data["daily"]["weathercode"][i],
            temp_min=data["daily"]["temperature_2m_min"][i],
            temp_max=data["daily"]["temperature_2m_max"][i],
            solar_energy=calculate_energy(data["daily"]["sunshine_duration"][i] / 3600)
        ))
    return forecasts


def build_summary(data: dict) -> WeeklySummary:
    temps_min = data["daily"]["temperature_2m_min"]
    temps_max = data["daily"]["temperature_2m_max"]
    sunshine = [s / 3600 for s in data["daily"]["sunshine_duration"]]
    precipitation = data["daily"]["precipitation_sum"]
    pressure = data["daily"].get("pressure_msl", [])

    summary_text = "z opadami" if sum(1 for p in precipitation if p > 0) >= 4 else "bez opadów"
    avg_pressure = round(sum(pressure) / len(pressure), 2) if pressure else None

    return WeeklySummary(
        avg_sunshine_duration=round(sum(sunshine) / len(sunshine), 2),
        min_temp=min(temps_min),
        max_temp=max(temps_max),
        summary=summary_text,
        avg_pressure_msl=avg_pressure
    )
