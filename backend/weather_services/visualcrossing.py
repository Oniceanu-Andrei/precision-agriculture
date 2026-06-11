import requests

def get_visualcrossing_forecast(lat: float, lon: float, api_key: str):
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{lat},{lon}/today"
    
    params = {
        "unitGroup": "metric",
        "include": "hours",
        "key": api_key,
        "contentType": "json"
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        forecast = []
        for item in data["days"][0]["hours"]:
            # datetime e de forma "00:00:00" - il transformam in timestamp complet
            date = data["days"][0]["datetime"]
            time = item["datetime"][:5]  # luam doar HH:MM
            
            forecast.append({
                "time": f"{date}T{time}",
                "temperature": item["temp"],
                "humidity": item["humidity"],
                "wind_speed": round(item["windspeed"] / 3.6, 1),  # km/h -> m/s
                "precipitation": item.get("precip", 0) or 0,
                "cloud_cover": item.get("cloudcover", 0)
            })
        
        return {
            "status": "success",
            "source": "VisualCrossing",
            "location": {"latitude": lat, "longitude": lon},
            "forecast": forecast
        }
    
    except Exception as e:
        return {
            "status": "error",
            "source": "VisualCrossing",
            "message": str(e)
        }