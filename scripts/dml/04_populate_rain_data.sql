-- ============================================
-- GRDC Database initialization script
-- Imports station metadata and daily flow data
-- ============================================
-- Load stations data
\COPY geodata.rain_stations (station_id, station_name, latitude, longitude) FROM '/tmp/rain_stations.csv' WITH CSV HEADER;

-- Load daily flow data
\COPY geodata.grdc_daily_flow (station_id, observation_date, value) FROM '/tmp/rain_data.csv' WITH CSV HEADER;

-- Log completion
DO $$
BEGIN
    RAISE NOTICE 'Rain_stations table populated with % rows', (SELECT COUNT(*) FROM geodata.rain_stations);
    RAISE NOTICE 'GRDC daily flow table populated with % rows', (SELECT COUNT(*) FROM geodata.rain_data);
END $$;
