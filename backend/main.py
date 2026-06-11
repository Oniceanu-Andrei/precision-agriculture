from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from weather_services.openmeteo import get_openmeteo_forecast
from weather_services.openweathermap import get_openweathermap_forecast
from weather_services.weatherapi import get_weatherapi_forecast
from weather_services.visualcrossing import get_visualcrossing_forecast
from weather_services.correlation import correlate_forecasts


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
OPENWEATHERMAP_API_KEY = "9c0a9e6046e9de78fb85473bec071329"
WEATHERAPI_API_KEY = "f56b9b1eaf734c8b8a6205654251011"
VISUALCROSSING_API_KEY = "SLSH5GJLK2HRK9VR6ZQDSHCMD"

# coordonatele centrului Romaniei
lat = 45.9432
lon = 24.9668

@app.get("/")
def home():
    return {"message": "Backend FastAPI functioneaza!"}

@app.get("/weather/openmeteo")
def get_weather_openmeteo():
    return get_openmeteo_forecast(lat, lon)

@app.get("/weather/openweathermap")
def get_weather_openweathermap():
    return get_openweathermap_forecast(lat, lon, OPENWEATHERMAP_API_KEY)

@app.get("/weather/weatherapi")
def get_weather_weatherapi():
    return get_weatherapi_forecast(lat, lon, WEATHERAPI_API_KEY)

@app.get("/weather/visualcrossing")
def get_weather_visualcrossing(lat: float = 45.9432, lon: float = 24.9668):
    return get_visualcrossing_forecast(lat, lon, VISUALCROSSING_API_KEY)

@app.get("/weather/correlated")
def get_correlated_weather(lat: float = 45.9432, lon: float = 24.9668):
    openmeteo = get_openmeteo_forecast(lat, lon)
    openweathermap = get_openweathermap_forecast(lat, lon, OPENWEATHERMAP_API_KEY)
    weatherapi = get_weatherapi_forecast(lat, lon, WEATHERAPI_API_KEY)
    visualcrossing = get_visualcrossing_forecast(lat, lon, VISUALCROSSING_API_KEY)
    
    return correlate_forecasts(openmeteo, openweathermap, weatherapi, visualcrossing)