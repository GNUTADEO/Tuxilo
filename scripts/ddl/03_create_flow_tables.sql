-- =====================================================
-- GRDC Stations Table
-- =====================================================
-- Stores station metadata extracted from GRDC Clean files
-- River:                 RIO SINU
-- Station:               COTOCA ABAJO  - AUT [13077060]
-- Latitude (DD):       9.224444444
-- Longitude (DD):      -75.83444444

CREATE TABLE IF NOT EXISTS geodata.flow_stations (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    latitude DECIMAL(10, 8) NOT NULL, 
    longitude DECIMAL(11, 8) NOT NULL 
);

CREATE INDEX IF NOT EXISTS idx_stations_name ON geodata.flow_stations(name);

-- =====================================================
-- GRDC Daily Flow Data Table
-- =====================================================
-- Stores daily river flow measurements from GRDC Clean files
-- YYYY-MM-DD;Value;month;Value_imputed
-- 1970-03-01;146.3;3;146.3

CREATE TABLE IF NOT EXISTS data.grdc_daily_flow (
    id BIGSERIAL PRIMARY KEY,
    station_id BIGSERIAL NOT NULL,
    observation_date DATE NOT NULL,
    value DECIMAL(12, 3),
    FOREIGN KEY (station_id) REFERENCES geodata.flow_stations(id) ON DELETE CASCADE,
    UNIQUE (station_id, observation_date)
);

CREATE INDEX IF NOT EXISTS idx_grdc_station_date ON data.grdc_daily_flow(station_id, observation_date);
CREATE INDEX IF NOT EXISTS idx_grdc_date ON data.grdc_daily_flow(observation_date);