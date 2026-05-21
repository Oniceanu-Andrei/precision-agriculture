import requests

def get_openmeteo_forecast(lat: float, lon: float):
    url = "https://api.open-meteo.com/v1/forecast"
    
    params = {  #specificam ce parametrii vrem din documentatia openmeteo
        "latitude": lat,
        "longitude": lon,
        "hourly": [
            "temperature_2m",
            "relative_humidity_2m",
            "wind_speed_10m",
            "precipitation",
            "pressure_msl",
            "cloud_cover"
        ],
        "timezone": "auto",
        "forecast_days": 1
    }
    
    try:                      # aici in request.get mai avem multi parametri optionali ,headers=None, cookies=None, etc
        response = requests.get(url, params=params, timeout=10) # request imi va returna un obiect de tip Response
        response.raise_for_status()   # Verificam statusul raspunsului , daca e !=200 , arunca exceptie. Avem timeout=10 ca sa nu asteptam
        data = response.json()   # deserealizam tot raspunsul json primit in response intr-un dictionar ca sa putem acesa datele 
        
        # Accesam datele

        hourly = data["hourly"]
        times = hourly["time"]
        temps = hourly["temperature_2m"]
        humidity = hourly["relative_humidity_2m"]
        wind = hourly["wind_speed_10m"]
        precipitation = hourly["precipitation"]
        pressure = hourly["pressure_msl"]
        clouds = hourly["cloud_cover"]
        
        forecast = []
        for i in range(len(times)):
            forecast.append({
                "time": times[i],
                "temperature": temps[i],
                "humidity": humidity[i],
                "wind_speed": wind[i],
                "precipitation": precipitation[i],
                "pressure": pressure[i],
                "cloud_cover": clouds[i]
            })
        
        return {
            "status": "success",
            "source": "Open-Meteo",
            "location": {"latitude": lat, "longitude": lon},
            "forecast": forecast
        }
    
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "source": "Open-Meteo",
            "message": f"Network error: {str(e)}"
        }
    
    except Exception as e:
        return {
            "status": "error",
            "source": "Open-Meteo",
            "message": f"Unexpected error: {str(e)}"
        }