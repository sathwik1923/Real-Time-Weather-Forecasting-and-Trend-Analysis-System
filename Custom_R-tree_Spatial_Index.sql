-- Ensure the PostGIS extension is enabled
CREATE EXTENSION IF NOT EXISTS postgis;

-- Create the spatial index
CREATE INDEX IF NOT EXISTS idx_weather_stations_location
ON weather_stations USING GIST (location);
