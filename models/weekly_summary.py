from pydantic import BaseModel


class WeeklySummary(BaseModel):
    avg_sunshine_duration: float
    min_temp: float
    max_temp: float
    summary: str
    avg_pressure: float
