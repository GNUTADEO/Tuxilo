-- ============================================
-- GRDC Database initialization script
-- Imports daily flow data
-- ============================================
-- Load stations data
\COPY geodata.flow_stations (station_id, station_name, latitude, longitude) FROM '/tmp/grdc_stations.csv' WITH CSV HEADER;

-- Load daily flow data
\COPY data.grdc_daily_flow (station_id, observation_date, value) FROM '/tmp/grdc_flow.csv' WITH CSV HEADER;

-- Log completion
DO $$
BEGIN
    RAISE NOTICE 'Flow_stations table populated with % rows', (SELECT COUNT(*) FROM geodata.flow_stations);
    RAISE NOTICE 'GRDC daily flow table populated with % rows', (SELECT COUNT(*) FROM data.grdc_daily_flow);
END $$;
