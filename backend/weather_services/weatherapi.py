import requests

def get_weatherapi_forecast(lat: float, lon: float, api_key: str):
    url = "https://api.weatherapi.com/v1/forecast.json"
    
    params = {
        "key": api_key,
        "q": f"{lat},{lon}",
        "days": 1,
        "aqi": "yes",
        "alerts": "no"
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        forecast = []
        for item in data["forecast"]["forecastday"][0]["hour"]:
            forecast.append({
                "time": item["time"],
                "temperature": item["temp_c"],
                "humidity": item["humidity"],
                "wind_speed": item["wind_kph"] / 3.6,
                "precipitation": item["precip_mm"],
                "cloud_cover": item["cloud"],
                "uv_index": item["uv"]
            })
        
        return {
            "status": "success",
            "source": "WeatherAPI",
            "location": {"latitude": lat, "longitude": lon},
            "forecast": forecast
        }
    
    except Exception as e:
        return {
            "status": "error",
            "source": "WeatherAPI",
            "message": str(e)
        }