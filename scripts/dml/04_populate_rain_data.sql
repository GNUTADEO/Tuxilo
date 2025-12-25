-- ============================================
-- GRDC Database initialization script
-- Imports station metadata and daily flow data
-- ============================================
-- Load stations data
\COPY geodata.rain_stations (station_id, river_name, station_name, latitude, longitude) FROM '/tmp/grdc_stations.csv' WITH CSV HEADER;

-- Load daily flow data
\COPY geodata.grdc_daily_flow (station_id, observation_date, flow_value, month_number, flow_value_imputed) FROM '/tmp/grdc_flow.csv' WITH CSV HEADER;

-- Log completion
DO $$
BEGIN
    RAISE NOTICE 'Rain_stations table populated with % rows', (SELECT COUNT(*) FROM geodata.rain_stations);
    RAISE NOTICE 'GRDC daily flow table populated with % rows', (SELECT COUNT(*) FROM geodata.grdc_daily_flow);
END $$;
