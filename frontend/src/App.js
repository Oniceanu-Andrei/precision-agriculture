import React, { useEffect, useState } from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

function App() {
  const [weatherData, setWeatherData] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/weather/openmeteo")
      .then(res => res.json())
      .then(data => setWeatherData(data.forecast))
      .catch(err => console.log(err));
  }, []);

  return (
  <div style={{ fontFamily: "Arial", padding: "30px" }}>
    <h1>Aplicație Agricultură de Precizie </h1>
    <h2>Prognoză temperatură Timișoara - 24 ore</h2>
    
    {}
    <ResponsiveContainer width="100%" height={400}>
      <LineChart data={weatherData}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="time" tickFormatter={(value) => value.slice(11, 16)}/>
        <YAxis label={{ value: 'Temperatura (°C)', angle: -90, position: 'insideLeft' }} />
        <Tooltip 
        labelFormatter = {(value)=>value.replace("T"," ").slice(0,16)}
        />
        <Legend />
        <Line type="monotone" dataKey="temperature" stroke="#82ca9d" strokeWidth={2} name="Temperatura" />
      </LineChart>
    </ResponsiveContainer>

    {}
    <h3 style={{ marginTop: "40px" }}>Detalii pe ore:</h3>
    <div style={{ 
      display: "grid", 
      gridTemplateColumns: "repeat(auto-fit, minmax(250px, 1fr))", 
      gap: "20px", 
      marginTop: "20px" 
    }}>
      {weatherData.map((item, index) => (
        <div 
          key={index} 
          style={{
            border: "1px solid #ccc",
            borderRadius: "10px",
            padding: "15px",
            boxShadow: "2px 2px 10px rgba(0,0,0,0.1)",
            backgroundColor: "#f9f9f9",
            textAlign: "center"
          }}
        >
    <h3>🕒 {item.time.replace("T", " ").slice(0, 16)}</h3>
    <p style={{ fontSize: "24px", fontWeight: "bold" }}>🌡️ {item.temperature}°C</p>
    {/* <p style={{ fontSize: "12px", color: "#666" }}>📍 {item.latitude.toFixed(2)}, {item.longitude.toFixed(2)}</p> */}
    </div>
    ))}
    </div>
  </div>
);
}

export default App;