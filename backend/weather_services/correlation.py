def correlate_forecasts(openmeteo_data, openweathermap_data, weatherapi_data):
    
    # Ponderi pentru fiecare sursa
    weights = {
        "openmeteo": 0.50,
        "openweathermap": 0.20,
        "weatherapi": 0.30
    }
    
    # Extragem forecast-urile din fiecare sursa
    openmeteo_forecast = openmeteo_data.get("forecast", []) if openmeteo_data.get("status") == "success" else []
    openweathermap_forecast = openweathermap_data.get("forecast", []) if openweathermap_data.get("status") == "success" else []
    weatherapi_forecast = weatherapi_data.get("forecast", []) if weatherapi_data.get("status") == "success" else []
    
    # Folosim orele din Open-Meteo ca referinta (are 24 ore)
    correlated = []
    
    for i, om_item in enumerate(openmeteo_forecast):
        hour = om_item["time"][11:13]  # extragem ora din timestamp
        
        # Gasim datele corespunzatoare din OpenWeatherMap (are date la fiecare 3 ore)
        owm_item = None
        for owm in openweathermap_forecast:
            if owm["time"][11:13] == hour:
                owm_item = owm
                break
        
        # Gasim datele corespunzatoare din WeatherAPI
        wa_item = None
        for wa in weatherapi_forecast:
            if wa["time"][11:13] == hour:
                wa_item = wa
                break
        
        # Calculam media ponderata pentru temperatura
        temp_values = []
        temp_weights = []
        
        if om_item:
            temp_values.append(om_item["temperature"])
            temp_weights.append(weights["openmeteo"])
        if owm_item:
            temp_values.append(owm_item["temperature"])
            temp_weights.append(weights["openweathermap"])
        if wa_item:
            temp_values.append(wa_item["temperature"])
            temp_weights.append(weights["weatherapi"])
        
        # Normalizam ponderile in caz ca lipseste o sursa
        total_weight = sum(temp_weights)
        if total_weight == 0:
            continue
            
        correlated_temp = sum(v * w for v, w in zip(temp_values, temp_weights)) / total_weight
        
        # Calculam media ponderata pentru umiditate
        humidity_values = []
        humidity_weights = []
        if om_item and "humidity" in om_item:
            humidity_values.append(om_item["humidity"])
            humidity_weights.append(weights["openmeteo"])
        if owm_item and "humidity" in owm_item:
            humidity_values.append(owm_item["humidity"])
            humidity_weights.append(weights["openweathermap"])
        if wa_item and "humidity" in wa_item:
            humidity_values.append(wa_item["humidity"])
            humidity_weights.append(weights["weatherapi"])
        
        total_humidity_weight = sum(humidity_weights)
        correlated_humidity = sum(v * w for v, w in zip(humidity_values, humidity_weights)) / total_humidity_weight if total_humidity_weight > 0 else None
        
        # Calculam media ponderata pentru vant
        wind_values = []
        wind_weights = []
        if om_item and "wind_speed" in om_item:
            wind_values.append(om_item["wind_speed"])
            wind_weights.append(weights["openmeteo"])
        if owm_item and "wind_speed" in owm_item:
            wind_values.append(owm_item["wind_speed"])
            wind_weights.append(weights["openweathermap"])
        if wa_item and "wind_speed" in wa_item:
            wind_values.append(wa_item["wind_speed"])
            wind_weights.append(weights["weatherapi"])
        
        total_wind_weight = sum(wind_weights)
        correlated_wind = sum(v * w for v, w in zip(wind_values, wind_weights)) / total_wind_weight if total_wind_weight > 0 else None
        
        # Calculam media ponderata pentru precipitatii
        precip_values = []
        precip_weights = []
        if om_item and "precipitation" in om_item:
            precip_values.append(om_item["precipitation"])
            precip_weights.append(weights["openmeteo"])
        if wa_item and "precipitation" in wa_item:
            precip_values.append(wa_item["precipitation"])
            precip_weights.append(weights["weatherapi"])
        
        total_precip_weight = sum(precip_weights)
        correlated_precip = sum(v * w for v, w in zip(precip_values, precip_weights)) / total_precip_weight if total_precip_weight > 0 else None
        
        correlated.append({
            "time": om_item["time"],
            "temperature": round(correlated_temp, 1),
            "humidity": round(correlated_humidity, 1) if correlated_humidity is not None else None,
            "wind_speed": round(correlated_wind, 1) if correlated_wind is not None else None,
            "precipitation": round(correlated_precip, 2) if correlated_precip is not None else None,
            "sources_used": {
                "openmeteo": om_item is not None,
                "openweathermap": owm_item is not None,
                "weatherapi": wa_item is not None
            }
        })
    
    return {
        "status": "success",
        "source": "Correlated",
        "weights": weights,
        "forecast": correlated
    }