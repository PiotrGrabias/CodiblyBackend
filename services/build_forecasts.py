from collections import defaultdict
from statistics import mean
from models.weather_forecast import WeatherForecast
from models.weekly_summary import WeeklySummary
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


def build_summary(daily_data: dict, pressure_data: dict) -> WeeklySummary:
    temps_min = daily_data["daily"]["temperature_2m_min"]
    temps_max = daily_data["daily"]["temperature_2m_max"]
    sunshine = [s / 3600 for s in daily_data["daily"]["sunshine_duration"]]
    precipitation = daily_data["daily"]["precipitation_sum"]

    pressure_by_day = defaultdict(list)
    try:
        times = pressure_data["hourly"]["time"]
        pressures = pressure_data["hourly"]["pressure_msl"]
        for t, p in zip(times, pressures):
            date = t.split("T")[0]
            pressure_by_day[date].append(p)

        daily_avg_pressures = [
            mean(pressure_by_day[date])
            for date in sorted(pressure_by_day.keys())[:7]
        ]
        avg_pressure = round(mean(daily_avg_pressures), 2)
    except Exception:
        avg_pressure = None

    summary_text = "z opadami" if sum(1 for p in precipitation if p > 50) >= 4 else "bez opadów"

    return WeeklySummary(
        avg_sunshine_duration=round(sum(sunshine) / len(sunshine), 2),
        min_temp=min(temps_min),
        max_temp=max(temps_max),
        summary=summary_text,
        avg_pressure=avg_pressure
    )