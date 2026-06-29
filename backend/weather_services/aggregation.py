def aggregate_forecasts(openmeteo_data, openweathermap_data, weatherapi_data, visualcrossing_data):
    
    weights = {
        "openmeteo": 0.30,
        "openweathermap": 0.10,
        "weatherapi": 0.20,
        "visualcrossing": 0.40
    }
    
    openmeteo_forecast = openmeteo_data.get("forecast", []) if openmeteo_data.get("status") == "success" else []
    openweathermap_forecast = openweathermap_data.get("forecast", []) if openweathermap_data.get("status") == "success" else []
    weatherapi_forecast = weatherapi_data.get("forecast", []) if weatherapi_data.get("status") == "success" else []
    visualcrossing_forecast = visualcrossing_data.get("forecast", []) if visualcrossing_data.get("status") == "success" else []
    
    aggregated = []
    
    for om_item in openmeteo_forecast:
        hour = om_item["time"][11:13]
        
        owm_item = None
        for owm in openweathermap_forecast:
            if owm["time"][11:13] == hour:
                owm_item = owm
                break
        
        wa_item = None
        for wa in weatherapi_forecast:
            if wa["time"][11:13] == hour:
                wa_item = wa
                break
        
        vc_item = None
        for vc in visualcrossing_forecast:
            if vc["time"][11:13] == hour:
                vc_item = vc
                break
        
        # Temperatura
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
        if vc_item:
            temp_values.append(vc_item["temperature"])
            temp_weights.append(weights["visualcrossing"])
        
        total_weight = sum(temp_weights)
        if total_weight == 0:
            continue
            
        aggregated_temp = sum(v * w for v, w in zip(temp_values, temp_weights)) / total_weight
        
        # Umiditate
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
        if vc_item and "humidity" in vc_item:
            humidity_values.append(vc_item["humidity"])
            humidity_weights.append(weights["visualcrossing"])
        
        total_humidity_weight = sum(humidity_weights)
        aggregated_humidity = sum(v * w for v, w in zip(humidity_values, humidity_weights)) / total_humidity_weight if total_humidity_weight > 0 else None
        
        # Vant
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
        if vc_item and "wind_speed" in vc_item:
            wind_values.append(vc_item["wind_speed"])
            weights_wind = weights["visualcrossing"]
            wind_weights.append(weights_wind)
        
        total_wind_weight = sum(wind_weights)
        aggregated_wind = sum(v * w for v, w in zip(wind_values, wind_weights)) / total_wind_weight if total_wind_weight > 0 else None
        
        # Precipitatii
        precip_values = []
        precip_weights = []
        if om_item and "precipitation" in om_item:
            precip_values.append(om_item["precipitation"])
            precip_weights.append(weights["openmeteo"])
        if owm_item and "precipitation" in owm_item:
            precip_values.append(owm_item["precipitation"])
            precip_weights.append(weights["openweathermap"])
        if wa_item and "precipitation" in wa_item:
            precip_values.append(wa_item["precipitation"])
            precip_weights.append(weights["weatherapi"])
        if vc_item and "precipitation" in vc_item:
            precip_values.append(vc_item["precipitation"])
            precip_weights.append(weights["visualcrossing"])
        
        total_precip_weight = sum(precip_weights)
        aggregated_precip = sum(v * w for v, w in zip(precip_values, precip_weights)) / total_precip_weight if total_precip_weight > 0 else None
        
        aggregated.append({
            "time": om_item["time"],
            "temperature": round(aggregated_temp, 1),
            "humidity": round(aggregated_humidity, 1) if aggregated_humidity is not None else None,
            "wind_speed": round(aggregated_wind, 1) if aggregated_wind is not None else None,
            "precipitation": round(aggregated_precip, 2) if aggregated_precip is not None else None,
            "sources_used": {
                "openmeteo": om_item is not None,
                "openweathermap": owm_item is not None,
                "weatherapi": wa_item is not None,
                "visualcrossing": vc_item is not None
            }
        })
    
    return {
        "status": "success",
        "source": "Aggregated",
        "weights": weights,
        "forecast": aggregated
    }