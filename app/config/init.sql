CREATE TABLE IF NOT EXISTS weather_alerts (
    id SERIAL PRIMARY KEY,
    city TEXT,
    timestamp BIGINT,
    temperature REAL,
    weather TEXT,
    humidity REAL,
    wind_speed REAL,
    is_alert BOOLEAN
);

CREATE INDEX IF NOT EXISTS idx_city ON weather_alerts(city);
CREATE INDEX IF NOT EXISTS idx_timestamp ON weather_alerts(timestamp);
