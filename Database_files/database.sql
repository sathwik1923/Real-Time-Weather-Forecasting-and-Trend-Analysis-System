CREATE EXTENSION postgis;

-- Table for storing raw weather JSON data
CREATE TABLE raw_weather_data (
    data_id SERIAL PRIMARY KEY,
    json_data JSONB,
    received_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Table for storing weather station information
CREATE TABLE weather_stations (
    station_id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE,
    country VARCHAR(50),
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    location GEOGRAPHY(Point, 4326)
);

-- Table for storing weather data
CREATE TABLE weather_data (
    data_id SERIAL PRIMARY KEY,
    station_id INTEGER REFERENCES weather_stations(station_id),
    timestamp TIMESTAMPTZ,
    temperature DOUBLE PRECISION,
    feels_like DOUBLE PRECISION,
    temp_min DOUBLE PRECISION,
    temp_max DOUBLE PRECISION,
    pressure INTEGER,
    humidity INTEGER,
    sea_level INTEGER,
    grnd_level INTEGER,
    visibility INTEGER,
    wind_speed DOUBLE PRECISION,
    wind_deg INTEGER,
    cloudiness INTEGER,
    weather_main VARCHAR(50),
    weather_description VARCHAR(100)
);

-- Table for storing weather forecasts
CREATE TABLE weather_forecasts (
    forecast_id SERIAL PRIMARY KEY,
    station_id INTEGER REFERENCES weather_stations(station_id),
    forecast_timestamp TIMESTAMPTZ,
    predicted_temperature DOUBLE PRECISION,
    predicted_humidity DOUBLE PRECISION,
    predicted_pressure DOUBLE PRECISION,
    forecast_description VARCHAR(100)
);
CREATE TABLE realtime_data(
    device_id VARCHAR,
    temperature FLOAT,
    humidity FLOAT,
    latitude FLOAT,
    longitude FLOAT
);
-- Spatial index for weather stations
CREATE INDEX idx_weather_stations_location
ON weather_stations USING GIST (location);
