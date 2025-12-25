-- =====================================================
-- GRDC Stations Table
-- =====================================================
-- Stores station metadata extracted from GRDC Clean files
-- River:                 RIO SINU
-- Station:               COTOCA ABAJO  - AUT [13077060]
-- Latitude (DD):       9.224444444
-- Longitude (DD):      -75.83444444

CREATE TABLE IF NOT EXISTS rain_stations (
    station_id VARCHAR(50) PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    river_name VARCHAR(255) NOT NULL,
    station_name VARCHAR(255) NOT NULL,
    latitude DECIMAL(10, 8) NOT NULL, --Por qué decimal y no NUMERIC?
    longitude DECIMAL(11, 8) NOT NULL --Por qué decimal y no NUMERIC?
);

CREATE INDEX IF NOT EXISTS idx_stations_river ON rain_stations(river_name);
CREATE INDEX IF NOT EXISTS idx_stations_name ON rain_stations(station_name);

-- =====================================================
-- GRDC Daily Flow Data Table
-- =====================================================
-- Stores daily river flow measurements from GRDC Clean files
-- YYYY-MM-DD;Value;month;Value_imputed
-- 1970-03-01;146.3;3;146.3

CREATE TABLE IF NOT EXISTS grdc_daily_flow (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    station_id VARCHAR(50) NOT NULL,
    observation_date DATE NOT NULL,
    flow_value DECIMAL(12, 3),
    month_number SMALLINT NOT NULL,
    flow_value_imputed DECIMAL(12, 3),
    FOREIGN KEY (station_id) REFERENCES rain_stations(station_id) ON DELETE CASCADE,
    UNIQUE (station_id, observation_date)
);

CREATE INDEX IF NOT EXISTS idx_grdc_station_date ON grdc_daily_flow(station_id, observation_date);
CREATE INDEX IF NOT EXISTS idx_grdc_date ON grdc_daily_flow(observation_date);
CREATE INDEX IF NOT EXISTS idx_grdc_month ON grdc_daily_flow(month_number);
