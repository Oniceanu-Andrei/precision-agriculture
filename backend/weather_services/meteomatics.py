import datetime as dt
import meteomatics.api as api

def get_meteomatics_forecast(lat: float, lon: float, username: str, password: str):
    
    params = {
        "coordinates": [(lat, lon)],
        "startdate": dt.datetime.utcnow(),
        "enddate": dt.datetime.utcnow() + dt.timedelta(hours=24),
        "interval": dt.timedelta(hours=1),
        "parameters": ["t_2m:C"]
    }

    try:
        df = api.query_time_series(  #df devine DataFrame atunci cand apelam metoda query_time_series(), un tip special de tabel
            params["coordinates"],
            params["startdate"],
            params["enddate"],
            params["interval"],
            params["parameters"],
            username,
            password
        )

        forecast = []
        for idx in range(len(df)):
            index_tuple = df.index[idx]
            lat_value = index_tuple[0]
            lon_value = index_tuple[1]
            timestamp = index_tuple[2] #obiect de tip Timestamp dim Pandas
            temp_value = df.iloc[idx, 0]
            
            forecast.append({   # salvam tot in dictionarul forecast
                "latitude": float(lat_value),
                "longitude": float(lon_value),#Convertim la float(), pentru ca Pandas returnează tipuri speciale (numpy.float64), deci convertim în float Python standard.
                "time": timestamp.isoformat(), # convertim timestamp in isoformat pentru ca JSON , nu poate stoca date TIMESTAMP
                "temperature": float(temp_value)
            })

        return {
            "status": "success",
            "source": "Meteomatics",
            "location": {"latitude": lat, "longitude": lon},
            "forecast": forecast  # Cand facem return se trimite ca si JSON , de aia a trebuit sa convertim obiectul timestamp
        }

    except Exception as e:
        return {
            "status": "error",
            "source": "Meteomatics",
            "message": str(e)
        }