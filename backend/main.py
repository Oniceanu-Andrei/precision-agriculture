from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from weather_services.openmeteo import get_openmeteo_forecast
from weather_services.meteomatics import get_meteomatics_forecast
from weather_services.openweathermap import get_openweathermap_forecast
from weather_services.weatherapi import get_weatherapi_forecast
from weather_services.correlation import correlate_forecasts


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

METEOMATICS_USERNAME = "acupt_oniceanu_andrei"
METEOMATICS_PASSWORD = "Vs64k1lUz9NzxVdM0zWY"
OPENWEATHERMAP_API_KEY = "9c0a9e6046e9de78fb85473bec071329"
WEATHERAPI_API_KEY = "f56b9b1eaf734c8b8a6205654251011"

lat = 45.737007
lon = 21.205186

@app.get("/")
def home():
    return {"message": "Backend FastAPI functioneaza!"}

@app.get("/weather/meteomatics")
def get_weather_meteomatics():
    return get_meteomatics_forecast(lat, lon, METEOMATICS_USERNAME, METEOMATICS_PASSWORD)

@app.get("/weather/openmeteo")
def get_weather_openmeteo():
    return get_openmeteo_forecast(lat, lon)

@app.get("/weather/openweathermap")
def get_weather_openweathermap():
    return get_openweathermap_forecast(lat, lon, OPENWEATHERMAP_API_KEY)

@app.get("/weather/weatherapi")
def get_weather_weatherapi():
    return get_weatherapi_forecast(lat, lon, WEATHERAPI_API_KEY)

@app.get("/weather/correlated")
def get_correlated_weather():
    openmeteo = get_openmeteo_forecast(lat, lon)
    openweathermap = get_openweathermap_forecast(lat, lon, OPENWEATHERMAP_API_KEY)
    weatherapi = get_weatherapi_forecast(lat, lon, WEATHERAPI_API_KEY)
    
    return correlate_forecasts(openmeteo, openweathermap, weatherapi)

@app.get("/weather/all")
def get_all_weather():
    return {
        "status": "success",
        "sources": {
            "meteomatics": get_weather_meteomatics(),
            "openmeteo": get_weather_openmeteo(),
            "openweathermap": get_weather_openweathermap(),
            "weatherapi": get_weather_weatherapi()
        }
    }