-- ============================================
-- GRDC Database initialization script
-- Imports station metadata and daily flow data
-- ============================================

-- Create tables if they don't exist
-- River:                 RIO SINU
-- Station:               COTOCA ABAJO  - AUT [13077060]
-- Latitude (DD):       9.224444444
-- Longitude (DD):      -75.83444444

CREATE TABLE IF NOT EXISTS stations (
    station_id VARCHAR(50) PRIMARY KEY,
    river_name VARCHAR(255) NOT NULL,
    station_name VARCHAR(255) NOT NULL,
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_stations_river ON stations(river_name);
CREATE INDEX IF NOT EXISTS idx_stations_name ON stations(station_name);

-- YYYY-MM-DD;Value;month;Value_imputed
-- 1970-03-01;146.3;3;146.3

CREATE TABLE IF NOT EXISTS grdc_daily_flow (
    id BIGSERIAL PRIMARY KEY,
    station_id VARCHAR(50) NOT NULL,
    observation_date DATE NOT NULL,
    flow_value DECIMAL(12, 3),
    month_number SMALLINT NOT NULL,
    flow_value_imputed DECIMAL(12, 3),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (station_id) REFERENCES stations(station_id) ON DELETE CASCADE,
    UNIQUE (station_id, observation_date)
);

CREATE INDEX IF NOT EXISTS idx_grdc_station_date ON grdc_daily_flow(station_id, observation_date);
CREATE INDEX IF NOT EXISTS idx_grdc_date ON grdc_daily_flow(observation_date);
CREATE INDEX IF NOT EXISTS idx_grdc_month ON grdc_daily_flow(month_number);

-- Load stations data
\COPY stations (station_id, river_name, station_name, latitude, longitude) FROM '/tmp/grdc_stations.csv' WITH CSV HEADER;

-- Load daily flow data
\COPY grdc_daily_flow (station_id, observation_date, flow_value, month_number, flow_value_imputed) FROM '/tmp/grdc_flow.csv' WITH CSV HEADER;

-- Log completion
DO $$
BEGIN
    RAISE NOTICE 'Stations table populated with % rows', (SELECT COUNT(*) FROM stations);
    RAISE NOTICE 'GRDC daily flow table populated with % rows', (SELECT COUNT(*) FROM grdc_daily_flow);
END $$;
