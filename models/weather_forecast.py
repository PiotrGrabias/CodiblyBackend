from pydantic import BaseModel


class WeatherForecast(BaseModel):
    date: str
    weather_code: int
    temp_min: float
    temp_max: float
    solar_energy: float