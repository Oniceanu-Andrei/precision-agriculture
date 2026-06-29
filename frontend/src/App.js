import React, { useEffect, useState } from "react";
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ReferenceLine
} from 'recharts';

const isAndroid = /android/i.test(navigator.userAgent);
const API_BASE = isAndroid 
  ? 'https://precision-agriculture-production.up.railway.app'
  : 'http://localhost:8000';

function App() {
const [weatherData, setWeatherData] = useState([]);
const [loading, setLoading] = useState(true);
const [locationName, setLocationName] = useState("Romania");
const [activeParam, setActiveParam] = useState("temperature");

const [searchCity, setSearchCity] = useState("");
const [searching, setSearching] = useState(false);

const isMobile = window.innerWidth < 768;

useEffect(() => {
  // Modificat: /weather/correlated -> /weather/aggregated
  fetch(`${API_BASE}/weather/aggregated`)
    .then(res => res.json())
    .then(data => {
      setWeatherData(data.forecast);
      setLoading(false);
    })
    .catch(err => alert("Eroare: " + err.message));
}, []);

const handleUseLocation = () => {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const { latitude, longitude } = position.coords;
        
        fetch(`https://nominatim.openstreetmap.org/reverse?lat=${latitude}&lon=${longitude}&format=json`)
          .then(res => res.json())
          .then(data => {
            const city = data.address.city || data.address.town || data.address.village || "Locatie necunoscuta";
            setLocationName(city);
          });

        setLoading(true);
        // Modificat: /weather/correlated -> /weather/aggregated
        fetch(`${API_BASE}/weather/aggregated?lat=${latitude}&lon=${longitude}`)
          .then(res => res.json())
          .then(data => {
            setWeatherData(data.forecast);
            setLoading(false);
          });
      },
      (error) => {
        alert("Locatia a fost refuzata!");
      }
    );
  } else {
    alert("Browserul tau nu suporta geolocation!");
  }
};

const handleCitySearch = async () => {
  if (!searchCity.trim()) return;
  setSearching(true);
  
  try {
    const geoResponse = await fetch(
      `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(searchCity)}&format=json&limit=1`
    );
    const geoData = await geoResponse.json();
    
    if (geoData.length === 0) {
      alert("Orasul nu a fost gasit!");
      setSearching(false);
      return;
    }
    
    const lat = parseFloat(geoData[0].lat);
    const lon = parseFloat(geoData[0].lon);
    const cityName = geoData[0].display_name.split(",")[0];
    
    setLocationName(cityName);
    setLoading(true);
    
    // Modificat: /weather/correlated -> /weather/aggregated
    const weatherResponse = await fetch(
      `${API_BASE}/weather/aggregated?lat=${lat}&lon=${lon}`
    );
    const weatherData = await weatherResponse.json();
    setWeatherData(weatherData.forecast);
    setLoading(false);
    setSearching(false);
    
  } catch (err) {
    console.log(err);
    setSearching(false);
    setLoading(false);
  }
};

useEffect(() => {
  const xhr = new XMLHttpRequest();
  // Modificat: /weather/correlated -> /weather/aggregated
  xhr.open('GET', `${API_BASE}/weather/aggregated`);
  xhr.onload = () => {
    const data = JSON.parse(xhr.responseText);
    setWeatherData(data.forecast);
    setLoading(false);
  };
  xhr.onerror = () => alert("XHR Eroare: " + xhr.status);
  xhr.send();
}, []);

  const params = [
    { key: "temperature", label: "Temperatura", unit: "°C", color: "#ff6b6b" },
    { key: "humidity", label: "Umiditate", unit: "%", color: "#4ecdc4" },
    { key: "wind_speed", label: "Vant", unit: "m/s", color: "#45b7d1" },
    { key: "precipitation", label: "Precipitatii", unit: "mm", color: "#96ceb4" },
  ];

  const activeParamInfo = params.find(p => p.key === activeParam);

  const getWeatherIcon = (item) => {
    if (item.precipitation > 0.5) return "🌧️";
    if (item.cloud_cover > 70) return "☁️";
    if (item.temperature > 25) return "☀️";
    if (item.temperature < 5) return "🥶";
    return "⛅";
  };

  if (loading) return (
    <div style={{
      display: "flex", justifyContent: "center", alignItems: "center",
      height: "100vh", background: "#0f172a", color: "white", fontSize: "24px"
    }}>
      Se incarca datele meteo...
    </div>
  );

  return (
    <div style={{ background: "#0f172a", minHeight: "100vh", color: "white", fontFamily: "Arial, sans-serif", overflowX: "hidden" }}>
      
      <div style={{
        background: "linear-gradient(135deg, #1e3a5f, #0f172a)",
        padding: isMobile ? "16px" : "30px 40px",
        borderBottom: "1px solid #1e293b"
      }}>
        <h1 style={{ margin: 0, fontSize: "28px", color: "#38bdf8" }}>
          🌾 Platforma Meteo pentru Agricultura de Precizie
        </h1>
        {/* Modificat mai jos: Date corelate -> Date agregate */}
        <p style={{ margin: "8px 0 0 0", color: "#94a3b8", fontSize: "14px" }}>
          📍 {locationName} | Date agregate din 4 surse: Visual Crossing (40%) · Open-Meteo (30%) · WeatherAPI (20%) · OpenWeatherMap (10%)
        </p>
        
        <div style={{ marginTop: "16px", display: "flex", gap: "8px", flexWrap: "wrap" }}>
          <input
            type="text"
            placeholder="Cauta un oras... (ex: Cluj-Napoca)"
            value={searchCity}
            onChange={(e) => setSearchCity(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleCitySearch()}
            style={{
              padding: "10px 16px",
              borderRadius: "8px",
              border: "1px solid #334155",
              background: "#1e293b",
              color: "white",
              fontSize: "14px",
              width: "300px",
              outline: "none"
            }}
          />
          <button
            onClick={handleCitySearch}
            disabled={searching}
            style={{
              padding: "10px 20px",
              borderRadius: "8px",
              border: "none",
              background: "#38bdf8",
              color: "#0f172a",
              fontSize: "14px",
              fontWeight: "bold",
              cursor: "pointer"
            }}
          >
            {searching ? "Se cauta..." : "🔍 Cauta"}
          </button>
          <button
            onClick={handleUseLocation}
            style={{
              padding: "10px 20px",
              borderRadius: "8px",
              border: "none",
              background: "#22c55e",
              color: "white",
              fontSize: "14px",
              fontWeight: "bold",
              cursor: "pointer"
            }}
          >
            📍 Locatia mea
          </button>
        </div>
      </div>

      <div style={{ padding: isMobile ? "16px" : "30px 40px" }}>

        {weatherData.length > 0 && (
          <div style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
            gap: "16px",
            marginBottom: "30px"
          }}>
            {params.map(param => {
              const currentValue = weatherData[new Date().getHours()]?.[param.key];
              return (
                <div
                  key={param.key}
                  onClick={() => setActiveParam(param.key)}
                  style={{
                    background: activeParam === param.key ? "#1e3a5f" : "#1e293b",
                    border: `2px solid ${activeParam === param.key ? param.color : "#334155"}`,
                    borderRadius: "12px",
                    padding: "20px",
                    cursor: "pointer",
                    transition: "all 0.2s"
                  }}
                >
                  <p style={{ margin: 0, color: "#94a3b8", fontSize: "13px" }}>{param.label}</p>
                  <p style={{ margin: "8px 0 0 0", fontSize: "28px", fontWeight: "bold", color: param.color }}>
                    {currentValue !== null && currentValue !== undefined
                      ? `${currentValue}${param.unit}`
                      : "N/A"}
                  </p>
                  <p style={{ margin: "4px 0 0 0", color: "#64748b", fontSize: "11px" }}>acum</p>
                </div>
              );
            })}
          </div>
        )}

        <div style={{
          background: "#1e293b",
          borderRadius: "12px",
          padding: "24px",
          marginBottom: "30px"
        }}>
          <h2 style={{ margin: "0 0 20px 0", color: "#e2e8f0", fontSize: "18px" }}>
            📈 {activeParamInfo?.label} — prognoza 24 ore
          </h2>
          <ResponsiveContainer width={isMobile ? "95%" : "100%"} height={300}>
            <LineChart data={weatherData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis
                dataKey="time"
                tickFormatter={(value) => value.slice(11, 16)}
                stroke="#64748b"
                tick={{ fill: "#94a3b8", fontSize: 12 }}
              />
              <YAxis
                stroke="#64748b"
                tick={{ fill: "#94a3b8", fontSize: 12 }}
                label={{
                  value: `${activeParamInfo?.label} (${activeParamInfo?.unit})`,
                  angle: -90,
                  position: 'insideLeft',
                  fill: "#94a3b8",
                  fontSize: 12
                }}
              />
              <Tooltip
                contentStyle={{ background: "#0f172a", border: "1px solid #334155", borderRadius: "8px" }}
                labelStyle={{ color: "#94a3b8" }}
                labelFormatter={(value) => value.replace("T", " ").slice(0, 16)}
                formatter={(value) => [`${value}${activeParamInfo?.unit}`, activeParamInfo?.label]}
              />
              <ReferenceLine
                x={weatherData[new Date().getHours()]?.time}
                stroke="#38bdf8"
                strokeWidth={2}
                strokeDasharray="3 3"
                label={{ value: "acum", fill: "#38bdf8", fontSize: 12 }}
              />
              <Line
                type="monotone"
                dataKey={activeParam}
                stroke={activeParamInfo?.color}
                strokeWidth={2}
                dot={false}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <h2 style={{ color: "#e2e8f0", fontSize: "18px", marginBottom: "16px" }}>
          🕒 Detalii pe ore
        </h2>
        <div style={{
          display: "grid",
          gridTemplateColumns: isMobile ? "repeat(2, 1fr)" : "repeat(auto-fit, minmax(180px, 1fr))",
          gap: "12px"
        }}>
          {weatherData.map((item, index) => {
            const isCurrentHour = parseInt(item.time.slice(11, 13)) === new Date().getHours();
            return (
              <div
                key={index}
                style={{
                  background: isCurrentHour ? "#1e3a5f" : "#1e293b",
                  border: `1px solid ${isCurrentHour ? "#38bdf8" : "#334155"}`,
                  borderRadius: "10px",
                  padding: isMobile ? "10px" : "16px",
                  textAlign: "center"
                }}
              >
                <p style={{ margin: 0, color: "#64748b", fontSize: "12px" }}>
                  {item.time.replace("T", " ").slice(0, 16)}
                </p>
                <p style={{ margin: "8px 0", fontSize: "28px" }}>
                  {getWeatherIcon(item)}
                </p>
                <p style={{ margin: "4px 0", color: "#ff6b6b", fontWeight: "bold", fontSize: "18px" }}>
                  {item.temperature}°C
                </p>
                <p style={{ margin: "2px 0", color: "#4ecdc4", fontSize: "13px" }}>
                  💧 {item.humidity}%
                </p>
                <p style={{ margin: "2px 0", color: "#45b7d1", fontSize: "13px" }}>
                  💨 {item.wind_speed} m/s
                </p>
                {item.precipitation > 0 && (
                  <p style={{ margin: "2px 0", color: "#96ceb4", fontSize: "13px" }}>
                    🌧️ {item.precipitation} mm
                  </p>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

export default App;