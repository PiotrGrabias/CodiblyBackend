import httpx
from fastapi import FastAPI, Path, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from models.forecast_response import ForecastResponse
from models.weekly_summary import WeeklySummary
from services.fetch_open_meteo import fetch_open_meteo, fetch_pressures
from services.build_forecasts import build_forecast, build_summary

app = FastAPI()
origin = [
    "https://codiblyfrontend.onrender.com"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/forecast/{lat}/{lon}", response_model=ForecastResponse)
async def current(
    lat: float = Path(..., description="Szerokość geograficzna", ge=-90.0, le=90.0),
    lon: float = Path(..., description="Długość geograficzna", ge=-180.0, le=180.0)
):
    try:
        data = await fetch_open_meteo(lat, lon)
        return {"forecast": build_forecast(data)}
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail="API Error")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/summary/{lat}/{lon}", response_model=WeeklySummary)
async def summary(lat: float, lon: float):
    try:
        daily_data, pressure_data = await fetch_open_meteo(lat, lon), await fetch_pressures(lat, lon)
        return build_summary(daily_data, pressure_data)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
