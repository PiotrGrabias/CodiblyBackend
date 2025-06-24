from pydantic import BaseModel
from typing import List
from models.weather_forecast import WeatherForecast


class ForecastResponse(BaseModel):
    forecast: List[WeatherForecast]