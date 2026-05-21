import requests

def get_openweathermap_forecast(lat: float, lon: float, api_key: str):
    url = "https://api.openweathermap.org/data/2.5/forecast"
    
    params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key,
        "units": "metric",
        "cnt": 8
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        forecast = []
        for item in data["list"]: # ne folosim doar de 'list' din data , mergem prin fiecare item
            forecast.append({         # primi direct grupate toate datele pe fiecare interval de ora
                "time": item["dt_txt"], # daca suntem la a n-a interatie de item , culegem al n-lea 'timp'
                "temperature": item["main"]["temp"],
                "humidity": item["main"]["humidity"],
                "wind_speed": item["wind"]["speed"],
                "pressure": item["main"]["pressure"],
                "description": item["weather"][0]["description"]  # aici e posibil sa avem o descriere mixa si o luam doar pe prima
            })                                                    # ex. rainy-cloudy , luam doar rainy, adica [0], prima pozitie
        
        return {
            "status": "success",
            "source": "OpenWeatherMap",
            "location": {"latitude": lat, "longitude": lon},
            "forecast": forecast
        }
    
    except Exception as e:
        return {
            "status": "error",
            "source": "OpenWeatherMap",
            "message": str(e)
        }